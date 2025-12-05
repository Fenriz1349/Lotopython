"""
data_fdj.py
-----------
Module responsible for managing all data operations related to FDJ lottery datasets.

This includes:
- Locating the data directory
- Loading local CSV files
- Updating datasets by downloading official FDJ archives
- Maintaining metadata (last update timestamp)

This file contains *only the structure* of the functions.
The internal logic will be added step by step.
"""

from pathlib import Path
import json
from typing import Dict, Any
import pandas as pd


# ---------------------------------------------------------
# Utility: get path to the data directory
# ---------------------------------------------------------
def get_data_dir() -> Path:
    """
    Returns the absolute path to the project's data directory.
    The folder contains all lottery CSV files and metadata.json.

    Returns:
        Path : absolute path to the data folder
    """
    return Path(__file__).resolve().parent.parent / "data"


# ---------------------------------------------------------
# Metadata management
# ---------------------------------------------------------
def get_last_update_date() -> str:
    """
    Reads metadata.json and extracts the last update date.

    Returns:
        str : date of the last update ("YYYY-MM-DD"), or "never" if no metadata exists.
    """
    data_dir = get_data_dir()
    metadata_file = data_dir / "metadata.json"

    if not metadata_file.exists():
        return "never"

    try:
        with open(metadata_file, "r") as f:
            meta = json.load(f)
            return meta.get("last_update", "never")
    except Exception:
        return "never"


def write_last_update_date(date_str: str) -> None:
    """
    Writes the last update timestamp into metadata.json.

    Args:
        date_str (str): date in format "YYYY-MM-DD"
    """
    data_dir = get_data_dir()
    metadata_file = data_dir / "metadata.json"

    metadata = {"last_update": date_str}

    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)


# ---------------------------------------------------------
# Load existing local CSV data
# ---------------------------------------------------------
def load_local_data() -> Dict[str, pd.DataFrame]:
    """
    Reads all CSV files stored in the data directory.
    Returns them as a dictionary of pandas DataFrames.

    Returns:
        dict[str, DataFrame] : dictionary containing datasets (loto, superloto, etc.)

    Note:
        Actual CSV parsing logic is not implemented yet.
    """

    datasets = {}

    # Example structure (implemented later):
    # datasets["loto"] = pd.read_csv(data_dir / "loto_2019_now.csv")

    return datasets


# ---------------------------------------------------------
# Update FDJ datasets (ZIP download → extract → convert)
# ---------------------------------------------------------
def update_data_from_fdj() -> bool:
    """
    Downloads the latest FDJ ZIP archives, extracts CSV files
    into the data directory, and updates metadata.

    Returns:
        bool : True if update success, False otherwise

    Note:
        Implementation will be added later.
    """
    # Placeholder for implementation
    return False
