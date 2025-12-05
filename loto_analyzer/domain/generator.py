# domain/generator.py

"""
Lottery draw generators (Loto and EuroMillions).

This module provides pure business logic for:
- random unique draws
- most/least frequent draws based on occurrence dictionaries
"""

import random
from typing import Dict, List
import pandas as pd


# ---------------------------------------------
#  Loto Generators
# ---------------------------------------------

def random_loto_unique(df: pd.DataFrame) -> List[int]:
    """
    Generate a Loto draw (5 numbers + chance number) that has never occurred.

    Args:
        df: DataFrame containing column 'combinaison_gagnante_en_ordre_croissant'.

    Returns:
        A unique draw as a list: [n1, n2, n3, n4, n5, chance]
    """
    while True:
        balls = sorted(random.sample(range(1, 50), 5))
        chance = random.randint(1, 10)

        draw_code = "-".join(map(str, balls)) + "+" + str(chance)

        if draw_code not in df["combinaison_gagnante_en_ordre_croissant"].values:
            return balls + [chance]


def loto_least_frequent(ball_occ: Dict[int, int], chance_occ: Dict[int, int]) -> List[int]:
    """
    Create a Loto draw using the least frequent numbers.

    Args:
        ball_occ: Occurrence count of balls.
        chance_occ: Occurrence count of 'numero_chance'.

    Returns:
        A list: 5 least frequent balls + least frequent chance number.
    """
    sorted_balls = sorted(ball_occ.items(), key=lambda x: x[1])
    sorted_chances = sorted(chance_occ.items(), key=lambda x: x[1])

    balls = [num for num, _ in sorted_balls[:5]]
    chance = sorted_chances[0][0]

    return balls + [chance]


def loto_most_frequent(ball_occ: Dict[int, int], chance_occ: Dict[int, int]) -> List[int]:
    """
    Create a Loto draw using the most frequent numbers.

    Args:
        ball_occ: Occurrence count of balls.
        chance_occ: Occurrence count of chance numbers.

    Returns:
        A list: 5 most frequent balls + most frequent chance number.
    """
    sorted_balls = sorted(ball_occ.items(), key=lambda x: x[1], reverse=True)
    sorted_chances = sorted(chance_occ.items(), key=lambda x: x[1], reverse=True)

    balls = [num for num, _ in sorted_balls[:5]]
    chance = sorted_chances[0][0]

    return balls + [chance]


# ---------------------------------------------
#  EuroMillions Generators
# ---------------------------------------------

def random_euromillions_unique(df: pd.DataFrame) -> List[int]:
    """
    Generate an EuroMillions draw that has never occurred.

    Args:
        df: DataFrame with columns:
            - 'boules_gagnantes_en_ordre_croissant'
            - 'etoiles_gagnantes_en_ordre_croissant'

    Returns:
        A list of 7 numbers: 5 balls + 2 stars.
    """
    while True:
        balls = sorted(random.sample(range(1, 51), 5))
        stars = sorted(random.sample(range(1, 13), 2))

        ball_code = "-".join(map(str, balls))
        star_code = "-".join(map(str, stars))

        if (
            ball_code not in df["boules_gagnantes_en_ordre_croissant"].values
            and star_code not in df["etoiles_gagnantes_en_ordre_croissant"].values
        ):
            return balls + stars


def euromillions_least_frequent(ball_occ: Dict[int, int], star_occ: Dict[int, int]) -> List[int]:
    """
    Create a EuroMillions draw using the least frequent balls and stars.

    Args:
        ball_occ: Occurrence dictionary for balls.
        star_occ: Occurrence dictionary for stars.

    Returns:
        A list of 7 numbers.
    """
    sorted_balls = sorted(ball_occ.items(), key=lambda x: x[1])
    sorted_stars = sorted(star_occ.items(), key=lambda x: x[1])

    balls = [num for num, _ in sorted_balls[:5]]
    stars = [num for num, _ in sorted_stars[:2]]

    return balls + stars


def euromillions_most_frequent(ball_occ: Dict[int, int], star_occ: Dict[int, int]) -> List[int]:
    """
    Create a EuroMillions draw using the most frequent balls and stars.

    Args:
        ball_occ: Occurrence dictionary for balls.
        star_occ: Occurrence dictionary for stars.

    Returns:
        A list of 7 numbers.
    """
    sorted_balls = sorted(ball_occ.items(), key=lambda x: x[1], reverse=True)
    sorted_stars = sorted(star_occ.items(), key=lambda x: x[1], reverse=True)

    balls = [num for num, _ in sorted_balls[:5]]
    stars = [num for num, _ in sorted_stars[:2]]

    return balls + stars