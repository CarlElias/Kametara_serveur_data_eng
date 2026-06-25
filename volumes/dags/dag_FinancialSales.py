from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
}

with DAG(
    dag_id="financial_sales_transactions",
    default_args=default_args,
    start_date=datetime(2026, 6, 24),
    schedule="*/5 * * * *",   # toutes les 5 minutes
    catchup=False,
) as dag:

    generate_transactions = BashOperator(
        task_id="generate_transactions",
        bash_command="""
        python /opt/airflow/dags/scripts_python/FinancialSales_Transactions.py
        """
    )