import pandas as pd
import pytest

from src.epra_validator import validate_epra_prices


def valid_prices():
    return pd.DataFrame(
        {
            "effective_from": [pd.Timestamp("2024-06-15")],
            "effective_to": [pd.Timestamp("2024-07-14")],
            "town": ["Nairobi"],
            "super_pms": [184.10],
            "diesel_ago": [171.20],
            "kerosene_ik": [156.30],
            "extracted_at": [pd.Timestamp("2024-06-15", tz="UTC")],
        }
    )


def test_validate_epra_prices_accepts_valid_data():
    validate_epra_prices(valid_prices())


def test_validate_epra_prices_rejects_duplicate_business_keys():
    duplicate_rows = pd.concat([valid_prices(), valid_prices()], ignore_index=True)

    with pytest.raises(ValueError, match="duplicate business-key"):
        validate_epra_prices(duplicate_rows)


def test_validate_epra_prices_rejects_negative_prices():
    invalid_prices = valid_prices()
    invalid_prices.loc[0, "diesel_ago"] = -1

    with pytest.raises(ValueError, match="negative diesel_ago"):
        validate_epra_prices(invalid_prices)


def test_validate_epra_prices_rejects_reversed_effective_dates():
    invalid_dates = valid_prices()
    invalid_dates.loc[0, "effective_to"] = pd.Timestamp("2024-06-14")

    with pytest.raises(ValueError, match="occurs before"):
        validate_epra_prices(invalid_dates)
