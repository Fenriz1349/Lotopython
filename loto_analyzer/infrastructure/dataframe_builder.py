# infrastructure/dataframe_builder.py

import os
import pandas as pd
from typing import List
from loto_analyzer.utils.constants import DAY_CONVERSION, EURO_COLUMNS_RENAME


DATA_DIR = "data"


def load_csv(path: str) -> pd.DataFrame:
    """
    Load an FDJ CSV using the correct delimiter and encoding.

    Args:
        path: Full path to the CSV file.

    Returns:
        A pandas DataFrame.
    """
    return pd.read_csv(path, delimiter=";", quotechar='"', encoding="latin-1")


def normalize_day_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize FDJ day codes (LU, MA, ME...) into full French day names.

    Args:
        df: DataFrame containing 'jour_de_tirage'.

    Returns:
        Modified DataFrame.
    """
    if "jour_de_tirage" in df.columns:
        df["jour_de_tirage"] = (
            df["jour_de_tirage"]
            .astype(str)
            .str.strip()
            .str.upper()
            .map(DAY_CONVERSION)
        )
    return df


def normalize_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert FDJ date format (integer like 20190417) into dd/mm/yyyy strings.

    Args:
        df: DataFrame containing 'date_de_tirage'.

    Returns:
        Modified DataFrame.
    """
    if "date_de_tirage" in df.columns:
        df["date_de_tirage"] = df["date_de_tirage"].astype(str).apply(
            lambda x: f"{x[-2:]}/{x[4:6]}/{x[0:4]}" if len(x) == 8 else x
        )
    return df


def clean_loto_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and unify a Loto CSV into a standard structure.

    Args:
        df: Raw DataFrame.

    Returns:
        A cleaned DataFrame ready for analysis.
    """
    drop_cols = [col for col in df.columns if "Unnamed" in col or "joker" in col.lower()]
    df = df.drop(columns=drop_cols, errors="ignore")

    df = normalize_day_column(df)
    df = normalize_date_column(df)

    if "annee_numero_de_tirage" in df.columns:
        df = df.sort_values(by="annee_numero_de_tirage")

    return df.reset_index(drop=True)


def clean_euromillions_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and unify an EuroMillions CSV into a standard structure.

    Args:
        df: Raw DataFrame.

    Returns:
        A cleaned DataFrame ready for analysis.
    """
    df = df.rename(columns=EURO_COLUMNS_RENAME)

    drop_cols = [col for col in df.columns if "Unnamed" in col or "joker" in col.lower()]
    df = df.drop(columns=drop_cols, errors="ignore")

    df = normalize_day_column(df)
    df = normalize_date_column(df)

    if "rapport_du_rang1" in df.columns:
        df["rapport_du_rang1"] = df["rapport_du_rang1"].astype(str).str.replace(" ", "")
        df["rapport_du_rang1"] = df["rapport_du_rang1"].astype(int)

    if "annee_numero_de_tirage" in df.columns:
        df = df.sort_values(by="annee_numero_de_tirage")

    return df.reset_index(drop=True)


def build_loto_dataframe() -> pd.DataFrame:
    """
    Load all Loto-related CSV files from the data directory,
    clean them, and return a single unified DataFrame.

    Returns:
        A cleaned and concatenated DataFrame for all Loto periods.
    """
    loto_files = [f for f in os.listdir(DATA_DIR) if "loto" in f.lower()]

    frames: List[pd.DataFrame] = []

    for file in loto_files:
        df = load_csv(os.path.join(DATA_DIR, file))
        frames.append(clean_loto_dataframe(df))

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)


def build_euromillions_dataframe() -> pd.DataFrame:
    """
    Load all EuroMillions CSV files from the data directory,
    clean them, and return a unified DataFrame.

    Returns:
        A cleaned and concatenated DataFrame.
    """
    euro_files = [f for f in os.listdir(DATA_DIR) if "euromillions" in f.lower()]

    frames: List[pd.DataFrame] = []

    for file in euro_files:
        df = load_csv(os.path.join(DATA_DIR, file))
        frames.append(clean_euromillions_dataframe(df))

    if not frames:
        return pd.DataFrame()

    return pd.concat(frames, ignore_index=True)
