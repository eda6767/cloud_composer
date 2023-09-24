
# Apache Airflow - Cloud Composer on GCP

<sub/>

<p align="center">
<img width="457" alt="Zrzut ekranu 2023-09-24 o 19 51 41" src="https://github.com/eda6767/dataproc/assets/102791467/a908775d-c855-4d84-af52-21b8c41acad6">

</p>

In this project we are going to create Cloud Composer environment and deploy DAG which contains creating container for Dataproc, 
<br/> 

running pipeline and shutting down container. 
<br/> 

This solution also will check if this is the first time when you run pipeline for given date or it is second time - then deleting data is executed.
<br/> 
<br/> 
<br/> 
<br/> 




<br/> 
<p align="center">
<img width="700" alt="Zrzut ekranu 2023-05-15 o 13 01 18" src="https://github.com/eda6767/airflow/assets/102791467/a4aea114-af3a-4dbe-80c4-661ca03ba420">
</p>


As a first step we will create Composer Environment. For this purpose we will set the minimum number of nodes which is - 3, and n1-stanard-1 as a machine type.

<br/> 
<br/> 
<p align="center">
<img width="600" alt="Zrzut ekranu 2023-05-15 o 13 02 11" src="https://github.com/eda6767/airflow/assets/102791467/a0574b3d-8478-4c6e-903b-a0081ca981b2">
</p>

After as environments has been created we can check DAG list, logs, DAG folder and also Aifrlow webserver. 

<br>

<p align="center">
<img width="600" alt="Zrzut ekranu 2023-05-15 o 13 02 47" src="https://github.com/eda6767/airflow/assets/102791467/c7c00d7e-487e-4493-aa85-639726f92d5e">
</p>
<br>

Now, we have to define first DAG. For this purpose we have to copy python file to DAG folder. This can be done throught console  or throught cloud shell. :shipit: 

<br><img width="1374" alt="Zrzut ekranu 2023-05-21 o 20 30 23 kopia" src="https://github.com/eda6767/airflow/assets/102791467/06cb2330-ba95-445d-855c-1cb53ef0605d">


After defining first dag, we are able to view a diagram in DAG list, in diagram section. We have first task, which starts pipeline containing DummyOperator. Next we are using 
<br/> 

branching which will check if there is the first running pipeline, or second, what means that we need to delete data from partition on BigQuery destination table. Afterward DAG 
<br/> 

creates cluster with given parameters, runs main ETL pipeline, and then deletes dataproc cluster.



<br/> 
<br/> 

<p align="center">
<img width="600" alt="Zrzut ekranu 2023-05-15 o 22 07 41" src="https://github.com/eda6767/airflow/assets/102791467/8c9ed6a1-7ec3-4b48-a03d-4605a27fff6d">
</p>
 
 
In contract to default BigQueryValueCheckOperator, BigQueryInsertJobOperator - for using BigQueryHook method we have to define connection in Airflow. For this purpose we are 
<br/> 

selecting Admin/ Connections.
<br/> 

<p align="center">
<img width="600" alt="Zrzut ekranu 2023-05-21 o 20 46 49" src="https://github.com/eda6767/airflow/assets/102791467/ba426fd5-0d06-4f97-a0eb-b0e2e9e0fadb">
</p>

For create needed connection we have to define a name - the same name will be used in DAG python file; option - Google Cloud and for Keyfile JSON File we will pass values from <br/>  

json generated for Service Account. Notice, that particular service account has to have permission required to viewing and selecting data from BigQuery.

<br/> <br/> 


<p align="center">
<img width="600" alt="Zrzut ekranu 2023-05-21 o 20 49 45" src="https://github.com/eda6767/airflow/assets/102791467/3dd1c0ae-2e1f-4d8d-bb4b-53dad1ac116a">
</p>


After finishing configuration, before saving I recommend to test the connection. In case of success we can finally save created configuration. Now this connection will be used <br/> 

with BigQueryHook method in DAGs.
<br/>
<br/> 


<p align="center">
<img width="600" alt="Zrzut ekranu 2023-05-21 o 20 50 22" src="https://github.com/eda6767/airflow/assets/102791467/bb2c2639-4452-4b31-99a4-7cea98152ed4">
</p>

After successfully completed task we should received DAG with status finished. Furthermore all instances used for running pipeline on dataproc should be deleted. 
<br/> 
<br/> 


<p align="center">
<img width="600" alt="Zrzut ekranu 2023-05-21 o 21 15 08" src="https://github.com/eda6767/airflow/assets/102791467/47b204b4-e302-4699-b112-f981755cb6af">
</p>


