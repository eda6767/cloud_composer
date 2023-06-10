# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:44:02 2023

@author: edytakorba
"""
from datetime import timedelta, datetime
from airflow import DAG 
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateClusterOperator,
    DataprocDeleteClusterOperator,
    DataprocSubmitJobOperator,
    ClusterGenerator)
from airflow.providers.google.cloud.sensors.dataproc import DataprocJobSensor
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator, BigQueryValueCheckOperator, BigQueryInsertJobOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.operators.python import BranchPythonOperator


GOOGLE_CONN_ID = "google_cloud_default"
PROJECT_ID="clean-sylph-377411"
BUCKET_NAME = 'dataproc_proc'
CLUSTER_NAME = 'dataproc-cluster'
REGION = 'europe-west1'
PYSPARK_URI = 'gs://dataproc_proc/dataproc.py'
DATASET = 'clean-sylph-377411.agr'
TABLE = 'dpcrnt_acct_trx_fcd'
DATE_ID='2021-10-31'

PYSPARK_JOB = {
    "reference": {"project_id": PROJECT_ID},
    "placement": {"cluster_name": CLUSTER_NAME},
    "pyspark_job": {"main_python_file_uri": PYSPARK_URI},
}

CLUSTER_CONFIG = ClusterGenerator(
    project_id=PROJECT_ID,
    zone="europe-west1-b",
    master_machine_type="n1-standard-2",
    worker_machine_type="n1-standard-2",
    init_actions_uris=['gs://goog-dataproc-initialization-actions-europe-west1/connectors/connectors.sh'],
    metadata = {'bigquery-connector-version':'1.2.0', 'spark-bigquery-connector-version':'0.21.0'},
    num_workers=2,
    worker_disk_size=500,
    master_disk_size=500,
    storage_bucket=BUCKET_NAME,
).make()

default_args = {
    'owner': 'DAR',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'start_date':  days_ago(2),
    'retry_delay': timedelta(minutes=5),
}



def big_query_check(**context):
    cursor = BigQueryHook(gcp_conn_id='bigquery_default').get_conn().cursor()

    #cursor.execute(SQL_QUERY)  # if non-legacy
    cursor.job_id = cursor.run_query(sql=SQL_QUERY, use_legacy_sql=False)  # if legacy
    result=cursor.fetchone()

    if results == 0:
        return "check_first_run"
    else:
        return "delete data"




SQL_QUERY=f"SELECT COUNT(*) FROM {DATASET}.{TABLE} WHERE DUE_DT='{DATE_ID}'"
sql = SQL_QUERY

with DAG('MCC_PROCEDURE', schedule_interval='@once', default_args=default_args) as dag:
    start_pipeline = DummyOperator(
        task_id = 'start_pipeline',
        dag = dag
        )
    check_first_run = BigQueryValueCheckOperator(
        task_id = 'check_first_run',
        sql=f"SELECT COUNT(*) FROM {DATASET}.{TABLE} WHERE DUE_DT='{DATE_ID}'",
        pass_value=0,
        use_legacy_sql=False,
        location=REGION
        )
    branch_task = BranchPythonOperator(
        task_id='branching', 
        python_callable=big_query_check,
        provide_context= True,
        templates_dict = {"sql": sql}
        )
    delete_data = BigQueryInsertJobOperator (
        task_id="insert_query_job",
        configuration={
                "query": {
                            "query": f"DELETE FROM {DATASET}.{TABLE} WHERE DUE_DT=' {DATE_ID}'",
                            "useLegacySql": False,
                    }
                    },
        location=REGION
        )
    create_cluster = DataprocCreateClusterOperator(
        task_id="create_cluster",
        project_id=PROJECT_ID,
        cluster_config=CLUSTER_CONFIG,
        region=REGION,
        cluster_name=CLUSTER_NAME,
        )
    pyspark_task = DataprocSubmitJobOperator(
        task_id="pyspark_task", 
        job=PYSPARK_JOB, 
        region=REGION, 
        project_id=PROJECT_ID,
        )
    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_cluster", 
        project_id=PROJECT_ID, 
        cluster_name=CLUSTER_NAME, 
        region=REGION,
        )
    finish_pipeline = DummyOperator(
        task_id = 'finish_pipeline',
        dag = dag
        )

#start_pipeline >> check_first_run >> create_cluster >> pyspark_task >> delete_cluster >> finish_pipeline
start_pipeline >> branch_task >> [delete_data , check_first_run ] >> create_cluster  >> pyspark_task >> delete_cluster >> finish_pipeline

