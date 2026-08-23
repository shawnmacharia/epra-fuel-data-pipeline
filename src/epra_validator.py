import pandas as pd

from src.config import (
    BUSINESS_KEY,
    PRICE_COLUMNS,
)


def validate_epra_prices(
    df: pd.DataFrame,
) -> None:
    """
    Validate the cleaned EPRA dataset.

    Raises ValueError if any critical data-quality
    rule fails.
    """

    print("Running data-quality checks...")

    # --------------------------------------------------------
    # Check DataFrame
    # --------------------------------------------------------

    if df.empty:
        raise ValueError(
            "Validation failed: DataFrame is empty."
        )

    # --------------------------------------------------------
    # Required columns
    # --------------------------------------------------------

    required_columns = (
        BUSINESS_KEY
        + PRICE_COLUMNS
        + ["extracted_at"]
    )

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Validation failed. Missing columns: "
            f"{missing_columns}"
        )

    # --------------------------------------------------------
    # Town validation
    # --------------------------------------------------------

    if df["town"].isna().any():
        raise ValueError(
            "Validation failed: missing town values."
        )

    if (
        df["town"]
        .astype(str)
        .str.strip()
        .eq("")
        .any()
    ):
        raise ValueError(
            "Validation failed: blank town values."
        )

    # --------------------------------------------------------
    # Date validation
    # --------------------------------------------------------

    for column in [
        "effective_from",
        "effective_to",
    ]:

        if df[column].isna().any():
            raise ValueError(
                f"Validation failed: invalid "
                f"{column} values."
            )

    # --------------------------------------------------------
    # Price validation
    # --------------------------------------------------------

    for column in PRICE_COLUMNS:

        if df[column].isna().any():
            raise ValueError(
                f"Validation failed: missing "
                f"{column} values."
            )

        if (df[column] < 0).any():
            raise ValueError(
                f"Validation failed: negative "
                f"{column} values."
            )

    # --------------------------------------------------------
    # Date logic
    # --------------------------------------------------------

    invalid_dates = (
        df["effective_to"]
        < df["effective_from"]
    )

    if invalid_dates.any():
        raise ValueError(
            "Validation failed: effective_to "
            "occurs before effective_from."
        )

    # --------------------------------------------------------
    # Duplicate business keys
    # --------------------------------------------------------

    duplicate_keys = df.duplicated(
        subset=BUSINESS_KEY,
        keep=False,
    )

    if duplicate_keys.any():

        duplicate_count = duplicate_keys.sum()

        raise ValueError(
            "Validation failed: "
            f"{duplicate_count} duplicate "
            "business-key rows detected."
        )

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    print(
        "ALL DATA-QUALITY CHECKS PASSED."
    )