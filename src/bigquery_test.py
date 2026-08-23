from google.cloud import bigquery
from datetime import datetime, timezone

PROJECT_ID = "epra-fuel-data-platform"
DATASET_ID = "epra_raw"
TABLE_ID = "airflow_connection_test"

def main():
    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    # 1. Create/Verify Table
    schema = [
        bigquery.SchemaField("message", "STRING"),
        bigquery.SchemaField("created_at", "TIMESTAMP"),
    ]

    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table, exists_ok=True)
    print(f"[SUCCESS] Verified table: {table.full_table_id}")

    # 2. Insert row using a Batch Load Job (Allowed in Sandbox/Free Tier)
    rows_to_insert = [
        {
            "message": "GCP BigQuery Connection Test OK",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Configure the job to append data
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition="WRITE_APPEND",
    )
    
    try:
        # This creates a batch load job, bypassing DML and Streaming restrictions
        load_job = client.load_table_from_json(
            rows_to_insert, table_ref, job_config=job_config
        )
        load_job.result()  # Wait for the job to complete
        
        print(f"[SUCCESS] Successfully loaded {load_job.output_rows} record(s) into BigQuery using a Batch Load Job!")
    except Exception as e:
        print(f"[ERROR] Failed to load row: {e}")

if __name__ == "__main__":
    main()