import pandas as pd
from sqlalchemy import text

from .postgres_loader import create_postgres_engine


def read_epra_prices_from_postgres() -> pd.DataFrame:
    """Read EPRA staging data from PostgreSQL."""
    engine = create_postgres_engine()

    query = text(
        """
        SELECT
            effective_from,
            effective_to,
            town,
            super_pms,
            diesel_ago,
            kerosene_ik,
            source_url,
            extracted_at,
            loaded_at
        FROM staging.epra_fuel_prices
        ORDER BY
            effective_from,
            town
        """
    )

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    if df.empty:
        raise ValueError("PostgreSQL staging table contains no EPRA records.")

    print(f"Read {len(df):,} rows from PostgreSQL.")
    return df