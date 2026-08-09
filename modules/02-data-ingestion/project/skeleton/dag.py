"""Airflow DAG stub — schedule the read-it-later pipeline (USE IT, lesson 01).

Requires Airflow installed (uv add apache-airflow). Not required to run the
plain-Python pipeline.py. TODO: point python_callable at your real pipeline.
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

default_args = {"retries": 2, "retry_delay": 300}


def run_pipeline():
    import subprocess
    subprocess.run(["python3", "pipeline.py"], check=True)


with DAG(
    "read_it_later",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:
    ingest = PythonOperator(task_id="ingest", python_callable=run_pipeline)
