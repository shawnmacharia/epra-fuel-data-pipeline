import os
from pathlib import Path
from dotenv import load_dotenv

# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

SAMPLE_DATA_DIR = DATA_DIR / "samples"


# ============================================================
# LOAD ENVIRONMENT VARIABLES (.env FROM PROJECT ROOT)
# ============================================================

load_dotenv(dotenv_path=PROJECT_ROOT / ".env")


# ============================================================
# EPRA SOURCE
# ============================================================

EPRA_URL = "https://www.epra.go.ke/pump-prices"


# ============================================================
# HTTP CONFIGURATION
# ============================================================

REQUEST_TIMEOUT = 30

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/151.0.0.0 Safari/537.36"
)


# ============================================================
# OUTPUT FILES
# ============================================================

CLEAN_OUTPUT_FILE = (
    PROCESSED_DATA_DIR / "epra_pump_prices_clean.csv"
)

RAW_OUTPUT_FILE = (
    RAW_DATA_DIR / "epra_pump_prices_raw.csv"
)


# ============================================================
# EXPECTED SOURCE COLUMNS
# ============================================================

EXPECTED_SOURCE_COLUMNS = {
    "From",
    "To",
    "Town",
    "Super (PMS)",
    "Diesel (AGO)",
    "Kerosene (IK)",
}


# ============================================================
# STANDARDIZED COLUMN NAMES
# ============================================================

COLUMN_MAPPING = {
    "From": "effective_from",
    "To": "effective_to",
    "Town": "town",
    "Super (PMS)": "super_pms",
    "Diesel (AGO)": "diesel_ago",
    "Kerosene (IK)": "kerosene_ik",
}


# ============================================================
# PRICE COLUMNS
# ============================================================

PRICE_COLUMNS = [
    "super_pms",
    "diesel_ago",
    "kerosene_ik",
]


# ============================================================
# BUSINESS KEY
# ============================================================

BUSINESS_KEY = [
    "effective_from",
    "effective_to",
    "town",
]


# ============================================================
# POSTGRESQL CONFIGURATION
# ============================================================

POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
    "localhost",
)

POSTGRES_PORT = os.getenv(
    "POSTGRES_PORT",
    "5432",
)

POSTGRES_DB = os.getenv(
    "POSTGRES_DB",
    "epra_dw",
)

POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
    "epra_user",
)

POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD",
    "",
)


# ============================================================
# GCP CONFIGURATION
# ============================================================

GCP_PROJECT_ID = os.getenv(
    "GCP_PROJECT_ID",
    "epra-fuel-data-platform",
)