from datetime import datetime, timezone

from sqlalchemy import text

from .postgres_loader import create_postgres_engine


def start_pipeline_run(
    pipeline_name: str,
) -> int:
    """
    Create a RUNNING record in the audit table.

    Returns
    -------
    int
        Newly created run ID.
    """

    engine = create_postgres_engine()

    started_at = datetime.now(timezone.utc)

    with engine.begin() as connection:

        result = connection.execute(
            text(
                """
                INSERT INTO audit.pipeline_runs (
                    pipeline_name,
                    started_at,
                    status
                )
                VALUES (
                    :pipeline_name,
                    :started_at,
                    'RUNNING'
                )
                RETURNING run_id
                """
            ),
            {
                "pipeline_name": pipeline_name,
                "started_at": started_at,
            },
        )

        run_id = result.scalar_one()

    return run_id


def complete_pipeline_run(
    run_id: int,
    status: str,
    rows_extracted: int = 0,
    rows_transformed: int = 0,
    rows_loaded: int = 0,
    error_message: str | None = None,
):
    """
    Complete an existing pipeline audit record.
    """

    if status not in {
        "SUCCESS",
        "FAILED",
    }:
        raise ValueError(
            "status must be SUCCESS or FAILED"
        )

    engine = create_postgres_engine()

    completed_at = datetime.now(timezone.utc)

    with engine.begin() as connection:

        connection.execute(
            text(
                """
                UPDATE audit.pipeline_runs

                SET
                    completed_at = :completed_at,
                    status = :status,
                    rows_extracted = :rows_extracted,
                    rows_transformed = :rows_transformed,
                    rows_loaded = :rows_loaded,
                    error_message = :error_message

                WHERE run_id = :run_id
                """
            ),
            {
                "run_id": run_id,
                "completed_at": completed_at,
                "status": status,
                "rows_extracted": rows_extracted,
                "rows_transformed": rows_transformed,
                "rows_loaded": rows_loaded,
                "error_message": error_message,
            },
        )