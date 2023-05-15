# airflow



python3 --version
python3 -m venv py_env
source py_env/bin/activate


pip install 'apache-airflow==2.6.0' \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.0/constraints-3.10.txt
 
 export AIRFLOW_HOME=.
 airflow db init
 
 airflow webserver -p 8080
 
