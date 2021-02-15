from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.email_operator import EmailOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.subdag_operator import SubDagOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime.today() - timedelta(days = 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
}

dag = DAG("MY_DAG", 
    default_args=default_args, 
    schedule_interval='@hourly', 
    max_active_runs=1, 
    catchup=False)

TASK_1 = BashOperator(task_id = 'TASK_1', bash_command = 'sleep 3' , dag = dag)
TASK_2 = BashOperator(task_id = 'TASK_2', bash_command = 'sleep 5' , dag = dag)

TASK_1.set_downstream(TASK_2)
