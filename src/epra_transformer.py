from datetime import datetime, timezone

import pandas as pd

from src.config import (
    COLUMN_MAPPING,
    PRICE_COLUMNS,
)


def clean_epra_prices(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Clean and standardize the raw EPRA price table.
    """

    df = df.copy()

    # --------------------------------------------------------
    # Rename source columns
    # --------------------------------------------------------

    df = df.rename(
        columns=COLUMN_MAPPING
    )

    # --------------------------------------------------------
    # Clean town names
    # --------------------------------------------------------

    df["town"] = (
        df["town"]
        .astype("string")
        .str.strip()
    )

    # --------------------------------------------------------
    # Convert dates
    # --------------------------------------------------------

    df["effective_from"] = pd.to_datetime(
        df["effective_from"],
        dayfirst=True,
        errors="coerce",
    )

    df["effective_to"] = pd.to_datetime(
        df["effective_to"],
        dayfirst=True,
        errors="coerce",
    )

    # --------------------------------------------------------
    # Convert fuel prices to numeric
    # --------------------------------------------------------

    for column in PRICE_COLUMNS:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    # --------------------------------------------------------
    # Remove completely empty rows
    # --------------------------------------------------------

    df = df.dropna(
        how="all"
    )

    # --------------------------------------------------------
    # Remove rows without a town
    # --------------------------------------------------------

    df = df[
        df["town"].notna()
    ]

    # --------------------------------------------------------
    # Remove exact duplicates
    # --------------------------------------------------------

    df = df.drop_duplicates()

    # --------------------------------------------------------
    # Add pipeline metadata
    # --------------------------------------------------------

    df["extracted_at"] = datetime.now(
        timezone.utc
    )

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    df = df.sort_values(
        [
            "effective_from",
            "town",
        ]
    ).reset_index(
        drop=True
    )

    return df