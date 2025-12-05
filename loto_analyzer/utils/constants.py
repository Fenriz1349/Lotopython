# utils/constants.py

# Mapping FDJ short day codes → French day names
DAY_CONVERSION = {
    "LU": "lundi",
    "MA": "mardi",
    "ME": "mercredi",
    "JE": "jeudi",
    "VE": "vendredi",
    "SA": "samedi",
}

# Mapping inconsistent EuroMillions column names → unified names
EURO_COLUMNS_RENAME = {
    "nombre_de_gagnant_au_rang1_Euro_Millions_en_france": "nombre_de_gagnant_au_rang1_en_france",
    "nombre_de_gagnant_au_rang1_Euro_Millions_en_europe": "nombre_de_gagnant_au_rang1_en_europe",
    "rapport_du_rang1_Euro_Millions": "rapport_du_rang1",
    "nombre_de_gagnant_au_rang2_Euro_Millions_en_france": "nombre_de_gagnant_au_rang2_en_france",
    "nombre_de_gagnant_au_rang2_Euro_Millions_en_europe": "nombre_de_gagnant_au_rang2_en_europe",
    "rapport_du_rang2_Euro_Millions": "rapport_du_rang2",
}
