from decimal import Decimal
import pandas as pd
from google.cloud import bigquery

from .config import GCP_PROJECT_ID

BIGQUERY_DATASET = "epra_raw"
BIGQUERY_TABLE = "epra_fuel_prices"


def create_bigquery_client() -> bigquery.Client:
    """Create an authenticated BigQuery client."""
    return bigquery.Client(project=GCP_PROJECT_ID)


def get_bigquery_table_id() -> str:
    """Return the fully qualified BigQuery target table ID."""
    return f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}"


def create_bigquery_table() -> bigquery.Table:
    """Create the raw EPRA table if it does not exist with partitioning and clustering."""
    client = create_bigquery_client()
    table_id = get_bigquery_table_id()

    schema = [
        bigquery.SchemaField("effective_from", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("effective_to", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("town", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("super_pms", "NUMERIC", mode="REQUIRED"),
        bigquery.SchemaField("diesel_ago", "NUMERIC", mode="REQUIRED"),
        bigquery.SchemaField("kerosene_ik", "NUMERIC", mode="REQUIRED"),
        bigquery.SchemaField("source_url", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("extracted_at", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("loaded_at", "TIMESTAMP", mode="REQUIRED"),
    ]

    table = bigquery.Table(table_id, schema=schema)

    # Partition by price effective date
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="effective_from",
    )

    # Cluster by town for dashboard performance
    table.clustering_fields = ["town"]

    table = client.create_table(table, exists_ok=True)
    print(f"BigQuery table ready: {table.full_table_id}")
    return table


def load_dataframe_to_bigquery(df: pd.DataFrame) -> int:
    """
    Idempotently load DataFrame to BigQuery raw table using Batch Load Job.
    Uses WRITE_TRUNCATE to comply with BigQuery Sandbox free tier limits.
    """
    if df.empty:
        print("DataFrame is empty. Nothing to load.")
        return 0

    create_bigquery_table()
    client = create_bigquery_client()
    table_id = get_bigquery_table_id()

    load_df = df.copy()

    # Enforce strict date and timestamp types
    load_df["effective_from"] = pd.to_datetime(load_df["effective_from"]).dt.date
    load_df["effective_to"] = pd.to_datetime(load_df["effective_to"]).dt.date
    load_df["extracted_at"] = pd.to_datetime(load_df["extracted_at"], utc=True)
    load_df["loaded_at"] = pd.to_datetime(load_df["loaded_at"], utc=True)

    # Cast float price columns to Python Decimal objects to match BigQuery NUMERIC (128-bit) schema
    price_cols = ["super_pms", "diesel_ago", "kerosene_ik"]
    for col in price_cols:
        load_df[col] = load_df[col].apply(
            lambda x: Decimal(str(x)) if pd.notna(x) and str(x).strip() != "" else None
        )

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        schema=[
            bigquery.SchemaField("effective_from", "DATE"),
            bigquery.SchemaField("effective_to", "DATE"),
            bigquery.SchemaField("town", "STRING"),
            bigquery.SchemaField("super_pms", "NUMERIC"),
            bigquery.SchemaField("diesel_ago", "NUMERIC"),
            bigquery.SchemaField("kerosene_ik", "NUMERIC"),
            bigquery.SchemaField("source_url", "STRING"),
            bigquery.SchemaField("extracted_at", "TIMESTAMP"),
            bigquery.SchemaField("loaded_at", "TIMESTAMP"),
        ],
    )

    # Batch load job (fully supported in BigQuery free tier sandbox)
    job = client.load_table_from_dataframe(load_df, table_id, job_config=job_config)
    job.result()

    print(f"BigQuery load completed: {len(load_df):,} rows written to {table_id}.")
    return len(load_df)