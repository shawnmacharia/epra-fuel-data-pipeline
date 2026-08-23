import os
from io import StringIO
import cloudscraper
import pandas as pd

from src.config import (
    EPRA_URL,
    EXPECTED_SOURCE_COLUMNS,
    REQUEST_TIMEOUT,
    USER_AGENT,
)


def download_epra_page() -> str:
    """
    Download the EPRA pump-price webpage using cloudscraper to bypass 403 firewalls,
    with a local fallback option if the network blocks it entirely.
    """
    sample_path = "data/samples/epra_sample.html"
    
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    try:
        print("Attempting bypass download of EPRA webpage...")
        response = scraper.get(
            EPRA_URL,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        html_content = response.text
        
    except Exception as e:
        print(f"Warning: Live bypass attempt failed ({e}). Falling back to local sample...")
        if os.path.exists(sample_path):
            with open(sample_path, "r", encoding="utf-8") as f:
                html_content = f.read()
        else:
            raise RuntimeError(
                f"Live firewall block encountered and no local fallback found at {sample_path}."
            )

    if not html_content.strip():
        raise ValueError("EPRA webpage content is empty.")

    return html_content


def _normalise_column_name(column) -> str:
    """
    Convert a source column name into a comparable format.
    """
    return " ".join(
        str(column)
        .replace("\n", " ")
        .split()
    ).strip()


def extract_price_table(html: str) -> pd.DataFrame:
    """
    Extract the EPRA fuel-price table from webpage HTML.
    """
    tables = pd.read_html(StringIO(html))

    if not tables:
        raise ValueError("No HTML tables were found on the EPRA webpage.")

    expected_normalised = {
        _normalise_column_name(column)
        for column in EXPECTED_SOURCE_COLUMNS
    }

    for table_number, table in enumerate(tables):
        table_columns = {
            _normalise_column_name(column)
            for column in table.columns
        }

        if expected_normalised.issubset(table_columns):
            print(f"EPRA price table found: table {table_number}")
            return table.copy()

    raise ValueError(
        "Could not locate the EPRA fuel-price table. "
        "The website structure may have changed."
    )


def extract_epra_prices() -> pd.DataFrame:
    """
    Complete extraction process.
    1. Download EPRA webpage (with cloudscraper/local fallback).
    2. Locate the fuel-price table.
    3. Return raw DataFrame.
    """
    print("Downloading EPRA webpage...")
    html = download_epra_page()

    print("Extracting EPRA price table...")
    df = extract_price_table(html)

    print(f"Extraction successful: {len(df):,} rows")
    return df