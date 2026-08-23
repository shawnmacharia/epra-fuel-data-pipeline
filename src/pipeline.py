from datetime import datetime, timezone

from src.config import (
    CLEAN_OUTPUT_FILE,
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
    RAW_OUTPUT_FILE,
)
from .epra_extractor import extract_epra_prices
from .epra_transformer import clean_epra_prices
from .epra_validator import validate_epra_prices
from .pipeline_audit import (
    complete_pipeline_run,
    start_pipeline_run,
)
from .postgres_loader import load_to_postgres


PIPELINE_NAME = "epra_fuel_prices"


def run_pipeline():

    start_time = datetime.now(
        timezone.utc
    )

    run_id = start_pipeline_run(
        PIPELINE_NAME
    )

    rows_extracted = 0
    rows_transformed = 0
    rows_loaded = 0

    print("=" * 70)
    print("EPRA FUEL PRICE DATA PIPELINE")
    print("=" * 70)

    print(f"Run ID: {run_id}")

    try:

        # ====================================================
        # PREPARE DIRECTORIES
        # ====================================================

        RAW_DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        PROCESSED_DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ====================================================
        # EXTRACT
        # ====================================================

        print("\n[1/5] EXTRACT")

        raw_df = extract_epra_prices()

        rows_extracted = len(raw_df)

        print(
            f"Rows extracted: "
            f"{rows_extracted:,}"
        )

        raw_df.to_csv(
            RAW_OUTPUT_FILE,
            index=False,
        )

        # ====================================================
        # TRANSFORM
        # ====================================================

        print("\n[2/5] TRANSFORM")

        clean_df = clean_epra_prices(
            raw_df
        )

        rows_transformed = len(clean_df)

        print(
            f"Rows transformed: "
            f"{rows_transformed:,}"
        )

        clean_df.to_csv(
            CLEAN_OUTPUT_FILE,
            index=False,
        )

        # ====================================================
        # VALIDATE
        # ====================================================

        print("\n[3/5] VALIDATE")

        validate_epra_prices(
            clean_df
        )

        # ====================================================
        # POSTGRES
        # ====================================================

        print("\n[4/5] POSTGRESQL LOAD")

        rows_loaded = load_to_postgres(
            clean_df
        )

        # ====================================================
        # COMPLETE AUDIT
        # ====================================================

        print("\n[5/5] AUDIT")

        complete_pipeline_run(
            run_id=run_id,
            status="SUCCESS",
            rows_extracted=rows_extracted,
            rows_transformed=rows_transformed,
            rows_loaded=rows_loaded,
        )

        end_time = datetime.now(
            timezone.utc
        )

        duration = (
            end_time - start_time
        ).total_seconds()

        print("\n" + "=" * 70)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 70)

        print(
            f"Run ID: {run_id}"
        )

        print(
            f"Extracted: {rows_extracted:,}"
        )

        print(
            f"Transformed: {rows_transformed:,}"
        )

        print(
            f"New rows loaded: {rows_loaded:,}"
        )

        print(
            f"Runtime: {duration:.2f} seconds"
        )

    except Exception as error:

        print("\nPIPELINE FAILED")

        complete_pipeline_run(
            run_id=run_id,
            status="FAILED",
            rows_extracted=rows_extracted,
            rows_transformed=rows_transformed,
            rows_loaded=rows_loaded,
            error_message=str(error),
        )

        raise


if __name__ == "__main__":
    run_pipeline()