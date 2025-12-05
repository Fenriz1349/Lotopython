# domain/stats.py

"""
Statistics utilities for analyzing FDJ lottery datasets.

This module contains pure business logic:
- occurrence calculations
- dataset cleaning adjustments
- lottery-specific statistical helpers
"""

from typing import Dict, List
import math
import pandas as pd


# ---------------------------------------------
#  Occurrence counters
# ---------------------------------------------

def count_ball_occurrences(df: pd.DataFrame) -> Dict[int, int]:
    """
    Count occurrences of main balls across all draw columns: boule_1, boule_2, ...

    Args:
        df: DataFrame containing FDJ draw data.

    Returns:
        A sorted dictionary {ball_number: occurrences}.
    """
    occurrences: Dict[int, int] = {}
    col_index = 1

    while True:
        col_name = f"boule_{col_index}"
        if col_name not in df.columns:
            break

        for value in df[col_name].values:
            if isinstance(value, (int, float)) and not math.isnan(value):
                value = int(value)
                occurrences[value] = occurrences.get(value, 0) + 1

        col_index += 1

    return dict(sorted(occurrences.items()))


def count_chance_occurrences(df: pd.DataFrame) -> Dict[int, int]:
    """
    Count occurrences of the Loto 'numero_chance'.

    Args:
        df: DataFrame.

    Returns:
        Dict of {chance_number: count}.
    """
    occurrences: Dict[int, int] = {}

    for value in df.get("numero_chance", []):
        if isinstance(value, (int, float)) and not math.isnan(value):
            value = int(value)
            occurrences[value] = occurrences.get(value, 0) + 1

    return dict(sorted(occurrences.items()))


def count_complementary_occurrences(df: pd.DataFrame) -> Dict[int, int]:
    """
    Count Loto complementary ball occurrences.

    Args:
        df: DataFrame.

    Returns:
        Dict of {ball_number: count}.
    """
    occurrences: Dict[int, int] = {}

    for value in df.get("boule_complementaire", []):
        if isinstance(value, (int, float)) and not math.isnan(value):
            value = int(value)
            occurrences[value] = occurrences.get(value, 0) + 1

    return dict(sorted(occurrences.items()))


def count_star_occurrences(df: pd.DataFrame) -> Dict[int, int]:
    """
    Count occurrences of EuroMillions stars: etoile_1, etoile_2.

    Args:
        df: DataFrame.

    Returns:
        Dict of {star_number: count}.
    """
    occurrences: Dict[int, int] = {}
    index = 1

    while True:
        col = f"etoile_{index}"
        if col not in df.columns:
            break

        for value in df[col]:
            if isinstance(value, (int, float)):
                occurrences[value] = occurrences.get(value, 0) + 1

        index += 1

    return dict(sorted(occurrences.items()))


# ---------------------------------------------
#  Winners and jackpot statistics
# ---------------------------------------------

def winners_by_day(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate total winners by day of draw and year.

    Args:
        df: DataFrame containing 'jour_de_tirage', 'date_de_tirage', 'nombre_de_gagnant_au_rang1'.

    Returns:
        A DataFrame grouped by year and draw day.
    """
    data = df.copy()

    # Convert date format yyyy/mm/dd → year
    data["annee"] = data["date_de_tirage"].str[-4:]

    # Harmonize column name for EuroMillions
    if "nombre_de_gagnant_au_rang1_en_europe" in data.columns:
        data = data.rename(
            columns={"nombre_de_gagnant_au_rang1_en_europe": "nombre_de_gagnant_au_rang1"}
        )

    data = data[["annee", "jour_de_tirage", "nombre_de_gagnant_au_rang1"]]

    return data.sort_values(by=["annee", "jour_de_tirage"])


def jackpot_by_day(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute mean jackpot (rapport_du_rang1) per year and per draw day.

    Args:
        df: DataFrame with jackpot information.

    Returns:
        A DataFrame aggregated by year and draw day.
    """
    data = df.copy()

    data["annee"] = data["date_de_tirage"].str[-4:]

    if "nombre_de_gagnant_au_rang1_en_europe" in data.columns:
        data = data.rename(
            columns={"nombre_de_gagnant_au_rang1_en_europe": "nombre_de_gagnant_au_rang1"}
        )

    data["rapport_du_rang1"] = data["rapport_du_rang1"].astype(int)

    data = data[["annee", "jour_de_tirage", "rapport_du_rang1", "nombre_de_gagnant_au_rang1"]]

    # Keep only rows where at least one person won
    data = data[data["nombre_de_gagnant_au_rang1"] > 0]

    return data.sort_values(by=["annee", "jour_de_tirage"])
