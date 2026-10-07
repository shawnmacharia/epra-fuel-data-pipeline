import os
from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

DATA_DIR = "/opt/airflow/data"
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw_epra_prices.csv")
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed_epra_prices.csv")


def extract_epra_task():
    """Extract raw fuel price data from EPRA and save it for downstream tasks."""
    from src.epra_extractor import extract_epra_prices

    df_raw = extract_epra_prices()
    os.makedirs(DATA_DIR, exist_ok=True)
    df_raw.to_csv(RAW_DATA_PATH, index=False)
    print(f"Extracted {len(df_raw):,} raw rows and saved to {RAW_DATA_PATH}")
    return len(df_raw)


def transform_data_task():
    """Clean and transform raw EPRA fuel price data."""
    from src.epra_transformer import clean_epra_prices

    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(f"Raw data file not found at {RAW_DATA_PATH}")

    df_raw = pd.read_csv(RAW_DATA_PATH)
    df_cleaned = clean_epra_prices(df_raw)
    os.makedirs(DATA_DIR, exist_ok=True)
    df_cleaned.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Transformed {len(df_cleaned):,} rows and saved to {PROCESSED_DATA_PATH}")
    return len(df_cleaned)


def validate_data_task():
    """Validate the transformed dataset schema and values."""
    from src.epra_validator import validate_epra_prices

    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError(f"Processed data file not found at {PROCESSED_DATA_PATH}")

    df_cleaned = pd.read_csv(PROCESSED_DATA_PATH)
    validate_epra_prices(df_cleaned)
    print("Validation passed successfully.")


def load_postgres_task():
    """Load validated data into PostgreSQL staging."""
    from src.postgres_loader import load_to_postgres

    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError(f"Processed data file not found at {PROCESSED_DATA_PATH}")

    df_cleaned = pd.read_csv(PROCESSED_DATA_PATH)
    rows_loaded = load_to_postgres(df_cleaned)
    print(f"Successfully loaded {rows_loaded:,} rows into PostgreSQL.")
    return rows_loaded


def start_pipeline_audit_task(**context):
    """Create an audit record for this Airflow DAG run."""
    from src.pipeline_audit import start_pipeline_run

    return start_pipeline_run(
        pipeline_name="epra_fuel_prices_pipeline",
        airflow_run_id=context["dag_run"].run_id,
    )


def complete_pipeline_audit_task(**context):
    """Mark this DAG run successful and persist task row counts."""
    from src.pipeline_audit import complete_pipeline_run

    task_instance = context["ti"]
    audit_run_id = task_instance.xcom_pull(task_ids="start_pipeline_audit")
    if audit_run_id is None:
        raise ValueError("Pipeline audit run ID was not created.")

    complete_pipeline_run(
        run_id=audit_run_id,
        status="SUCCESS",
        rows_extracted=task_instance.xcom_pull(task_ids="extract_epra") or 0,
        rows_transformed=task_instance.xcom_pull(task_ids="transform_data") or 0,
        rows_loaded=task_instance.xcom_pull(task_ids="load_postgres") or 0,
    )


def mark_pipeline_audit_failed(context):
    """Record a failed Airflow task against its DAG-run audit row."""
    from src.pipeline_audit import complete_pipeline_run

    task_instance = context["ti"]
    audit_run_id = task_instance.xcom_pull(task_ids="start_pipeline_audit")
    if audit_run_id is None:
        return

    exception = context.get("exception")
    complete_pipeline_run(
        run_id=audit_run_id,
        status="FAILED",
        rows_extracted=task_instance.xcom_pull(task_ids="extract_epra") or 0,
        rows_transformed=task_instance.xcom_pull(task_ids="transform_data") or 0,
        rows_loaded=task_instance.xcom_pull(task_ids="load_postgres") or 0,
        error_message=str(exception)[:4000] if exception else "Airflow task failed.",
    )


def load_bigquery_task():
    """Load the PostgreSQL snapshot to the BigQuery raw table."""
    from src.bigquery_loader import load_dataframe_to_bigquery
    from src.postgres_reader import read_epra_prices_from_postgres

    df = read_epra_prices_from_postgres()
    rows_loaded = load_dataframe_to_bigquery(df)
    print(f"Successfully loaded {rows_loaded:,} rows into BigQuery.")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": mark_pipeline_audit_failed,
}

with DAG(
    dag_id="epra_fuel_prices_pipeline",
    default_args=default_args,
    description="EPRA fuel prices pipeline, scheduled during the monthly pricing cycle",
    schedule_interval="0 0 15-31 * *",
    start_date=datetime(2026, 1, 15),
    catchup=False,
    max_active_runs=1,
    tags=["EPRA", "fuel", "data-engineering", "daily"],
) as dag:
    start_pipeline_audit = PythonOperator(
        task_id="start_pipeline_audit",
        python_callable=start_pipeline_audit_task,
    )

    extract_epra = PythonOperator(
        task_id="extract_epra",
        python_callable=extract_epra_task,
    )

    transform_data = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data_task,
    )

    validate_data = PythonOperator(
        task_id="validate_data",
        python_callable=validate_data_task,
    )

    load_postgres = PythonOperator(
        task_id="load_postgres",
        python_callable=load_postgres_task,
    )

    load_bigquery = PythonOperator(
        task_id="load_bigquery",
        python_callable=load_bigquery_task,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            "cd /opt/airflow/dbt/epra_warehouse && "
            "/home/airflow/.local/bin/dbt build --profiles-dir /opt/airflow/dbt"
        ),
        execution_timeout=timedelta(minutes=20),
        append_env=True,
        env={
            "GOOGLE_APPLICATION_CREDENTIALS": "/opt/airflow/credentials/epra-airflow.json"
        },
    )

    complete_pipeline_audit = PythonOperator(
        task_id="complete_pipeline_audit",
        python_callable=complete_pipeline_audit_task,
    )

    (
        start_pipeline_audit
        >> extract_epra
        >> transform_data
        >> validate_data
        >> load_postgres
        >> load_bigquery
        >> dbt_build
        >> complete_pipeline_audit
    )
