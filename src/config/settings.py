import os
from pathlib import Path

SRC_DIR = Path(__file__).parent.parent
ROOT_DIR = SRC_DIR.parent
FILE_JSON_NAME = "geo_data.json"
FILE_JSON_PATH = ROOT_DIR / FILE_JSON_NAME

# ======================
# Database configuration
# ======================
POSTGRES_NAME = os.getenv("POSTGRES_DB", default="postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", default="postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", default=5432)
POSTGRES_USER = os.getenv("POSTGRES_USER", default="postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", default="postgres")

DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_NAME}"

TABLE_NAME = f"countries_{os.getenv('SOURCE', default='')}"


# ====================
# parser configuration
# ====================
PARSERS_MAPPING = {
    "wikipedia": "ParserWiki",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}

# ====================
# API configuration
# ====================
# url
API_URL = "http://api.geonames.org/countryInfoJSON"

USERNAME = os.getenv("GEO_API_USERNAME")
PARAMS = {
    "formatted": "true",
    "lang": "en",
    "username": USERNAME,
    "style": "full",
}
