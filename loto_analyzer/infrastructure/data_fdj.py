# infrastructure/data_fdj.py

import os
import json
import requests
from zipfile import ZipFile
from datetime import datetime
from typing import Dict, List


DATA_DIR = "data"
METADATA_FILE = os.path.join(DATA_DIR, "metadata.json")


LOTO_URLS = {
    "1976_2008": "https://media.fdj.fr/static-draws/csv/loto/loto_197605.zip",
    "2008_2017": "https://media.fdj.fr/static-draws/csv/loto/loto_200810.zip",
    "2017_2019": "https://media.fdj.fr/static-draws/csv/loto/loto_201703.zip",
    "2019_transition": "https://media.fdj.fr/static-draws/csv/loto/loto_201902.zip",
    "2019_now": "https://media.fdj.fr/static-draws/csv/loto/loto_201911.zip",
    "super_1996_2008": "https://media.fdj.fr/static-draws/csv/loto/superloto_199605.zip",
    "super_2008_2017": "https://media.fdj.fr/static-draws/csv/loto/superloto_200810.zip",
    "super_2017_2019": "https://media.fdj.fr/static-draws/csv/loto/superloto_201703.zip",
    "super_2019_now": "https://media.fdj.fr/static-draws/csv/loto/superloto_201907.zip",
    "noel_2017_now": "https://media.fdj.fr/static-draws/csv/loto/lotonoel_201703.zip",
    "grandloto_2019_now": "https://media.fdj.fr/static-draws/csv/loto/grandloto_201912.zip",
}

EUROMILLIONS_URLS = {
    "2004_2011": "https://media.fdj.fr/static-draws/csv/euromillions/euromillions_200402.zip",
    "2011_2014": "https://media.fdj.fr/static-draws/csv/euromillions/euromillions_201105.zip",
    "2014_2016": "https://media.fdj.fr/static-draws/csv/euromillions/euromillions_201402.zip",
    "2016_2019": "https://media.fdj.fr/static-draws/csv/euromillions/euromillions_201609.zip",
    "2019_2020": "https://media.fdj.fr/static-draws/csv/euromillions/euromillions_201902.zip",
    "2020_now": "https://media.fdj.fr/static-draws/csv/euromillions/euromillions_202002.zip",
}


def ensure_data_directory() -> None:
    """Create the data directory if it does not already exist."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_metadata() -> Dict:
    """Load metadata.json or return a default metadata structure."""
    if not os.path.exists(METADATA_FILE):
        return {"last_update": None, "files": {}}

    with open(METADATA_FILE, "r") as f:
        return json.load(f)


def save_metadata(metadata: Dict) -> None:
    """Write metadata.json to disk."""
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=4)


def download_zip(url: str, output_path: str) -> None:
    """Download a ZIP file from a given FDJ URL."""
    response = requests.get(url, timeout=15)

    if response.status_code != 200:
        raise RuntimeError(f"Download failed for {url}")

    with open(output_path, "wb") as f:
        f.write(response.content)


def extract_zip(zip_path: str, target_dir: str) -> List[str]:
    """Extract all CSV files from a ZIP archive."""
    with ZipFile(zip_path, "r") as z:
        z.extractall(target_dir)
        return z.namelist()


def update_fdj_data() -> None:
    """
    Download all FDJ datasets (Loto + EuroMillions),
    extract the CSV files into the data directory,
    update metadata.json, and remove ZIP archives.
    """
    ensure_data_directory()
    metadata = load_metadata()
    now = datetime.now().isoformat()

    urls = {**LOTO_URLS, **EUROMILLIONS_URLS}

    for _, url in urls.items():
        zip_name = url.split("/")[-1]
        zip_path = os.path.join(DATA_DIR, zip_name)

        download_zip(url, zip_path)
        extract_zip(zip_path, DATA_DIR)

        metadata["files"][zip_name] = now
        os.remove(zip_path)

    metadata["last_update"] = now
    save_metadata(metadata)
