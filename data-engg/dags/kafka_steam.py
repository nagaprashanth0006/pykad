import datetime
from airflow import DAG
from airflow.operators.python imrpot PythonOperator

default_args = {
    "owner": "prashanth",
    "start_date": datetime.datetime.today() - datetime.timedelta(days = 60)
}
def stream_data():
    pass

with DAG('user_automation',
         default_args = default_args,
         schedule_interval="@daily",
         catchup=False) as dag:
    streaming_task = PythonOperator(
        task_id = "stream_data_from_api"
        python_callable = stream_data
    )