"""DAG de Airflow: orquesta ingesta/transformación (PySpark), dbt y validación.

Flujo:  generar_datos >> pyspark_pipeline >> dbt_run >> dbt_test >> publicar_metricas
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

PROJECT = "/opt/airflow/project"

default_args = {
    "owner": "data-eng",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="ventas_pipeline",
    description="Pipeline de ventas: PySpark + dbt + validaciones",
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["ventas", "final"],
) as dag:
    generar_datos = BashOperator(
        task_id="generar_datos",
        bash_command=f"cd {PROJECT} && python data/generate_data.py",
    )

    pyspark_pipeline = BashOperator(
        task_id="pyspark_pipeline",
        bash_command=f"cd {PROJECT} && python run_pipeline.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {PROJECT}/dbt_project && dbt run --profiles-dir .",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {PROJECT}/dbt_project && dbt test --profiles-dir .",
    )

    publicar_metricas = BashOperator(
        task_id="publicar_metricas",
        bash_command=f"cp {PROJECT}/output/pipeline_metrics.prom /textfile/ || true",
    )

    generar_datos >> pyspark_pipeline >> dbt_run >> dbt_test >> publicar_metricas
