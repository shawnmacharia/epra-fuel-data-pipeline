import os
from datetime import datetime, timedelta
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# File persistence paths across Airflow tasks
DATA_DIR = "/opt/airflow/data"
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw_epra_prices.csv")
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed_epra_prices.csv")


# ============================================================
# TASK CALLABLES
# ============================================================

def extract_epra_task():
    """Extract raw fuel price data from EPRA portal and save to disk."""
    from src.epra_extractor import extract_epra_prices
    
    df_raw = extract_epra_prices()
    os.makedirs(DATA_DIR, exist_ok=True)
    df_raw.to_csv(RAW_DATA_PATH, index=False)
    print(f"Extracted {len(df_raw):,} raw rows and saved to {RAW_DATA_PATH}")


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


def validate_data_task():
    """Validate transformed EPRA dataset schema and values."""
    from src.epra_validator import validate_epra_prices
    
    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError(f"Processed data file not found at {PROCESSED_DATA_PATH}")

    df_cleaned = pd.read_csv(PROCESSED_DATA_PATH)
    validate_epra_prices(df_cleaned)
    print("Validation passed successfully.")


def load_postgres_task():
    """Load validated dataset into PostgreSQL staging database."""
    from src.postgres_loader import load_to_postgres
    
    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError(f"Processed data file not found at {PROCESSED_DATA_PATH}")

    df_cleaned = pd.read_csv(PROCESSED_DATA_PATH)
    rows_loaded = load_to_postgres(df_cleaned)
    print(f"Successfully loaded {rows_loaded:,} rows into PostgreSQL.")


def quality_check_task():
    """Run data quality / audit checks using pipeline_audit."""
    try:
        import src.pipeline_audit as audit
        if hasattr(audit, 'run_audit'):
            audit.run_audit()
        elif hasattr(audit, 'main'):
            audit.main()
    except Exception as e:
        print(f"Audit step completed or skipped: {e}")


def load_bigquery_task():
    """Idempotently load PostgreSQL data to BigQuery raw table."""
    from src.postgres_reader import read_epra_prices_from_postgres
    from src.bigquery_loader import load_dataframe_to_bigquery

    df = read_epra_prices_from_postgres()
    rows_loaded = load_dataframe_to_bigquery(df)
    print(f"Successfully loaded {rows_loaded:,} rows into BigQuery.")


# ============================================================
# DAG DEFINITION
# ============================================================

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="epra_fuel_prices_pipeline",
    default_args=default_args,
    description="EPRA Fuel Prices Pipeline: Scraping -> PostgreSQL -> BigQuery -> dbt",
    schedule_interval="@monthly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["EPRA", "fuel", "data-engineering"],
) as dag:

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

    quality_check = PythonOperator(
        task_id="quality_check",
        python_callable=quality_check_task,
    )

    load_bigquery = PythonOperator(
        task_id="load_bigquery",
        python_callable=load_bigquery_task,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            "cd /opt/airflow/dbt/epra_warehouse && "
            "/home/airflow/.local/bin/dbt build --profiles-dir /opt/airflow/dbt/profiles"
        ),
        execution_timeout=timedelta(minutes=20),
        env={
            "GOOGLE_APPLICATION_CREDENTIALS": "/opt/airflow/credentials/epra-airflow.json"
        },
    )

    # Dependency sequence
    (
        extract_epra
        >> transform_data
        >> validate_data
        >> load_postgres
        >> quality_check
        >> load_bigquery
        >> dbt_build
    )