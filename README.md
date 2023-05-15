# airflow


```
python3 --version
python3 -m venv py_env
source py_env/bin/activate

https://github.com/apache/airflow 
pip install 'apache-airflow==2.6.0' \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.0/constraints-3.10.txt
 
 export AIRFLOW_HOME=.
 airflow db init
 
 airflow webserver -p 8080
 
 
 export AIRFLOW_HOME=~/airflow
 airflow webserver -p 8080
 
 
 airflow users create --username admin --firstname firstname --lastname lastname --role Admin --email admin@domain.com
 

```
 
