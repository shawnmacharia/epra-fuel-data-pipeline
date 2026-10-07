import pandas as pd

from src.epra_transformer import clean_epra_prices


def test_clean_epra_prices_standardizes_sorts_and_preserves_input():
    raw = pd.DataFrame(
        {
            "From": ["15/06/2024", "15/06/2024"],
            "To": ["14/07/2024", "14/07/2024"],
            "Town": [" Nairobi ", "Kisumu"],
            "Super (PMS)": [184.10, "180.50"],
            "Diesel (AGO)": [171.20, "168.75"],
            "Kerosene (IK)": [156.30, "155.00"],
        }
    )
    original_columns = list(raw.columns)

    cleaned = clean_epra_prices(raw)

    assert list(raw.columns) == original_columns
    assert cleaned["town"].tolist() == ["Kisumu", "Nairobi"]
    assert cleaned["effective_from"].tolist() == [
        pd.Timestamp("2024-06-15"),
        pd.Timestamp("2024-06-15"),
    ]
    assert pd.api.types.is_numeric_dtype(cleaned["super_pms"])
    assert cleaned["extracted_at"].dt.tz is not None
