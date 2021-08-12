from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    "owner": "despik",
    "start_date": days_ago(1),  # запуск день назад
    "retries": 5,  # запуск таска до 5 раз, если ошибка
    #"email" : ["artomonik@mail.ru"],
    #"retry_delay": datetime.timedelta(minutes=5),  # дельта запуска при повторе 5 минут
    #"task_concurency": 1  # одновременно только 1 таск
}

pipelines = {'print_info': {"schedule": "1 * * * *"},
            "plot": {"schedule": "1 * * * *"},
            "regression": {"schedule": "1 * * * *"}}


def init_dag(dag, task_id):
    with dag:
        t1 = BashOperator(
            task_id=f"{task_id}",
            bash_command=f'python3 /usr/local/airflow/code/{task_id}.py')
    return dag


for task_id, params in pipelines.items():
    # DAG - ациклический граф
    dag = DAG(task_id,
              schedule_interval=params['schedule'],
              max_active_runs=1,
              default_args=default_args
              )
    init_dag(dag, task_id)
    globals()[task_id] = dag