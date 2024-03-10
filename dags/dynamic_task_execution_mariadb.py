from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.time_delta import TimeDeltaSensor
from datetime import datetime, timedelta
import mariadb
import json

# 데이터베이스 설정 - 실제 값으로 대체 필요
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root123',
    'database': 'airflow_tasks_db'
}

default_args = {
    'owner': 'airflow',
    'start_date': datetime.now() - timedelta(days=10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dynamic_task_execution_mariadb',
    default_args=default_args,
    schedule_interval='@daily',
)

def fetch_tasks():
    """데이터베이스에서 작업 목록을 조회합니다."""
    tasks_info = []
    try:
        conn = mariadb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT task_name, task_params FROM task_info WHERE workflow_id = %s", ('workflow_1',))
        for task_name, task_params in cursor:
            tasks_info.append({
                'task_name': task_name,
                'task_params': json.loads(task_params)  # JSON 문자열을 Python 객체로 변환
            })
        cursor.close()
        conn.close()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    return tasks_info

def execute_task(task_name, task_params):
    """실제 작업을 실행하는 함수."""
    print(f"Executing {task_name} with params {task_params}")

tasks_info = fetch_tasks()  # 데이터베이스에서 작업 정보 조회

previous_task = None
for task_info in tasks_info:
    task_name = task_info['task_name']
    task_params = task_info['task_params']

    if task_name == 'wait_30m':
        op = TimeDeltaSensor(
            task_id='wait_30m',
            delta=timedelta(minutes=30),
            dag=dag,
        )
    else:
        op = PythonOperator(
            task_id=task_name,
            python_callable=execute_task,
            op_kwargs={'task_name': task_name, 'task_params': task_params},
            dag=dag,
        )

    if previous_task:
        previous_task >> op  # 이전 작업과 현재 작업 간 의존성 설정
    previous_task = op
