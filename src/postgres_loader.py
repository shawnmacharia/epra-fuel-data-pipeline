from datetime import datetime, timezone

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from .config import (
    EPRA_URL,
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)


def create_postgres_engine():
    """
    Create a SQLAlchemy connection to PostgreSQL.
    """
    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=int(POSTGRES_PORT),
        database=POSTGRES_DB,
    )

    return create_engine(
        connection_url,
        pool_pre_ping=True,
    )


def load_to_postgres(
    df: pd.DataFrame,
) -> int:
    """
    Load EPRA fuel-price data into PostgreSQL using UPSERT.

    New records are inserted.

    Existing records matching the primary key:
        effective_from + effective_to + town

    are updated with the latest values.

    Returns the number of rows processed.
    """

    # ---------------------------------------------------------
    # 1. Validate input
    # ---------------------------------------------------------
    if df.empty:
        raise ValueError(
            "Cannot load an empty DataFrame."
        )

    # Required columns
    required_columns = [
        "effective_from",
        "effective_to",
        "town",
        "super_pms",
        "diesel_ago",
        "kerosene_ik",
        "extracted_at",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    # ---------------------------------------------------------
    # 2. Create PostgreSQL connection
    # ---------------------------------------------------------
    engine = create_postgres_engine()

    # ---------------------------------------------------------
    # 3. Prepare load data
    # ---------------------------------------------------------
    load_time = datetime.now(timezone.utc)

    load_df = df.copy()

    # Add source metadata
    load_df["source_url"] = EPRA_URL
    load_df["loaded_at"] = load_time

    # ---------------------------------------------------------
    # 4. Remove duplicate keys inside the DataFrame
    # ---------------------------------------------------------
    # This is an additional safety check.
    #
    # The database primary key is:
    # effective_from + effective_to + town
    #
    # The CSV should already be unique, but keeping this
    # validation makes the loader safer.
    # ---------------------------------------------------------
    duplicate_mask = load_df.duplicated(
        subset=[
            "effective_from",
            "effective_to",
            "town",
        ],
        keep=False,
    )

    duplicate_count = duplicate_mask.sum()

    if duplicate_count > 0:
        duplicate_rows = (
            load_df.loc[
                duplicate_mask,
                [
                    "effective_from",
                    "effective_to",
                    "town",
                ],
            ]
            .drop_duplicates()
        )

        raise ValueError(
            "Duplicate primary-key records detected "
            f"in input data: {duplicate_count} rows.\n"
            f"Duplicate keys:\n{duplicate_rows.to_string(index=False)}"
        )

    # ---------------------------------------------------------
    # 5. Keep only database columns
    # ---------------------------------------------------------
    load_df = load_df[
        [
            "effective_from",
            "effective_to",
            "town",
            "super_pms",
            "diesel_ago",
            "kerosene_ik",
            "source_url",
            "extracted_at",
            "loaded_at",
        ]
    ]

    # ---------------------------------------------------------
    # 6. PostgreSQL UPSERT statement
    # ---------------------------------------------------------
    #
    # If the record does NOT exist:
    #     INSERT
    #
    # If the record already exists:
    #     UPDATE the fuel prices and metadata
    #
    # The conflict key is:
    #     effective_from
    #     effective_to
    #     town
    # ---------------------------------------------------------
    upsert_sql = text(
        """
        INSERT INTO staging.epra_fuel_prices (
            effective_from,
            effective_to,
            town,
            super_pms,
            diesel_ago,
            kerosene_ik,
            source_url,
            extracted_at,
            loaded_at
        )
        VALUES (
            :effective_from,
            :effective_to,
            :town,
            :super_pms,
            :diesel_ago,
            :kerosene_ik,
            :source_url,
            :extracted_at,
            :loaded_at
        )

        ON CONFLICT (
            effective_from,
            effective_to,
            town
        )

        DO UPDATE SET
            super_pms = EXCLUDED.super_pms,
            diesel_ago = EXCLUDED.diesel_ago,
            kerosene_ik = EXCLUDED.kerosene_ik,
            source_url = EXCLUDED.source_url,
            extracted_at = EXCLUDED.extracted_at,
            loaded_at = EXCLUDED.loaded_at
        """
    )

    # ---------------------------------------------------------
    # 7. Execute UPSERT
    # ---------------------------------------------------------
    processed_count = 0

    with engine.begin() as connection:

        for _, row in load_df.iterrows():

            row_dict = row.to_dict()

            # Convert pandas/numpy values into Python values
            # that psycopg2 can safely handle.
            for key, value in row_dict.items():

                if hasattr(value, "to_pydatetime"):
                    row_dict[key] = value.to_pydatetime()

                elif hasattr(value, "item"):
                    row_dict[key] = value.item()

            connection.execute(
                upsert_sql,
                row_dict,
            )

            processed_count += 1

    # ---------------------------------------------------------
    # 8. Report result
    # ---------------------------------------------------------
    print(
        f"Successfully processed: "
        f"{processed_count:,} rows"
    )

    print(
        "Mode: PostgreSQL UPSERT "
        "(INSERT new / UPDATE existing)"
    )

    return processed_count