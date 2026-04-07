"""
Static country GDP data — IMF/World Bank estimates, 2023.
gdp_nominal  : Nominal GDP in USD billions
gdp_real     : Real GDP in constant 2015 USD billions (approximate)
population   : Population in millions
gdp_per_capita: Nominal GDP per capita in USD
"""

import pandas as pd

COUNTRIES = [
    # North America
    {"country": "United States",    "region": "North America",  "gdp_nominal": 27360, "gdp_real": 22100, "population": 335.9,  "gdp_per_capita": 81695},
    {"country": "Canada",           "region": "North America",  "gdp_nominal": 2120,  "gdp_real": 1750,  "population": 40.1,   "gdp_per_capita": 52830},
    {"country": "Mexico",           "region": "North America",  "gdp_nominal": 1460,  "gdp_real": 1150,  "population": 128.5,  "gdp_per_capita": 11360},
    # South America
    {"country": "Brazil",           "region": "South America",  "gdp_nominal": 2130,  "gdp_real": 1800,  "population": 215.3,  "gdp_per_capita": 9893},
    {"country": "Argentina",        "region": "South America",  "gdp_nominal": 640,   "gdp_real": 550,   "population": 45.4,   "gdp_per_capita": 14097},
    {"country": "Colombia",         "region": "South America",  "gdp_nominal": 360,   "gdp_real": 300,   "population": 51.9,   "gdp_per_capita": 6937},
    {"country": "Chile",            "region": "South America",  "gdp_nominal": 340,   "gdp_real": 290,   "population": 19.5,   "gdp_per_capita": 17436},
    {"country": "Peru",             "region": "South America",  "gdp_nominal": 270,   "gdp_real": 220,   "population": 33.4,   "gdp_per_capita": 8084},
    # Europe
    {"country": "Germany",          "region": "Europe",         "gdp_nominal": 4430,  "gdp_real": 3650,  "population": 84.4,   "gdp_per_capita": 52497},
    {"country": "United Kingdom",   "region": "Europe",         "gdp_nominal": 3090,  "gdp_real": 2700,  "population": 67.7,   "gdp_per_capita": 45647},
    {"country": "France",           "region": "Europe",         "gdp_nominal": 2780,  "gdp_real": 2500,  "population": 68.2,   "gdp_per_capita": 40760},
    {"country": "Italy",            "region": "Europe",         "gdp_nominal": 2170,  "gdp_real": 1850,  "population": 58.9,   "gdp_per_capita": 36818},
    {"country": "Russia",           "region": "Europe",         "gdp_nominal": 2010,  "gdp_real": 1600,  "population": 144.8,  "gdp_per_capita": 13890},
    {"country": "Spain",            "region": "Europe",         "gdp_nominal": 1420,  "gdp_real": 1250,  "population": 47.4,   "gdp_per_capita": 29962},
    {"country": "Netherlands",      "region": "Europe",         "gdp_nominal": 1120,  "gdp_real": 900,   "population": 17.9,   "gdp_per_capita": 62566},
    {"country": "Turkey",           "region": "Europe",         "gdp_nominal": 1030,  "gdp_real": 900,   "population": 85.3,   "gdp_per_capita": 12079},
    {"country": "Switzerland",      "region": "Europe",         "gdp_nominal": 870,   "gdp_real": 680,   "population": 8.8,    "gdp_per_capita": 98924},
    {"country": "Poland",           "region": "Europe",         "gdp_nominal": 690,   "gdp_real": 600,   "population": 36.7,   "gdp_per_capita": 18805},
    {"country": "Belgium",          "region": "Europe",         "gdp_nominal": 630,   "gdp_real": 520,   "population": 11.7,   "gdp_per_capita": 53846},
    {"country": "Sweden",           "region": "Europe",         "gdp_nominal": 600,   "gdp_real": 490,   "population": 10.5,   "gdp_per_capita": 57134},
    {"country": "Ireland",          "region": "Europe",         "gdp_nominal": 550,   "gdp_real": 380,   "population": 5.1,    "gdp_per_capita": 107843},
    {"country": "Norway",           "region": "Europe",         "gdp_nominal": 550,   "gdp_real": 380,   "population": 5.5,    "gdp_per_capita": 100000},
    {"country": "Austria",          "region": "Europe",         "gdp_nominal": 530,   "gdp_real": 430,   "population": 9.1,    "gdp_per_capita": 58242},
    {"country": "Denmark",          "region": "Europe",         "gdp_nominal": 400,   "gdp_real": 310,   "population": 5.9,    "gdp_per_capita": 67797},
    {"country": "Romania",          "region": "Europe",         "gdp_nominal": 300,   "gdp_real": 240,   "population": 19.0,   "gdp_per_capita": 15789},
    {"country": "Czech Republic",   "region": "Europe",         "gdp_nominal": 300,   "gdp_real": 230,   "population": 10.9,   "gdp_per_capita": 27523},
    {"country": "Finland",          "region": "Europe",         "gdp_nominal": 305,   "gdp_real": 240,   "population": 5.6,    "gdp_per_capita": 54464},
    {"country": "Portugal",         "region": "Europe",         "gdp_nominal": 270,   "gdp_real": 230,   "population": 10.2,   "gdp_per_capita": 26471},
    {"country": "Greece",           "region": "Europe",         "gdp_nominal": 240,   "gdp_real": 195,   "population": 10.4,   "gdp_per_capita": 23077},
    {"country": "Ukraine",          "region": "Europe",         "gdp_nominal": 160,   "gdp_real": 130,   "population": 37.4,   "gdp_per_capita": 4278},
    {"country": "Hungary",          "region": "Europe",         "gdp_nominal": 200,   "gdp_real": 160,   "population": 9.7,    "gdp_per_capita": 20619},
    # Asia
    {"country": "China",            "region": "Asia",           "gdp_nominal": 17795, "gdp_real": 15400, "population": 1409.7, "gdp_per_capita": 12621},
    {"country": "Japan",            "region": "Asia",           "gdp_nominal": 4230,  "gdp_real": 4600,  "population": 124.5,  "gdp_per_capita": 33950},
    {"country": "India",            "region": "Asia",           "gdp_nominal": 3730,  "gdp_real": 2800,  "population": 1428.6, "gdp_per_capita": 2611},
    {"country": "South Korea",      "region": "Asia",           "gdp_nominal": 1710,  "gdp_real": 1550,  "population": 51.7,   "gdp_per_capita": 33073},
    {"country": "Indonesia",        "region": "Asia",           "gdp_nominal": 1370,  "gdp_real": 1100,  "population": 277.5,  "gdp_per_capita": 4941},
    {"country": "Thailand",         "region": "Asia",           "gdp_nominal": 510,   "gdp_real": 420,   "population": 71.8,   "gdp_per_capita": 7104},
    {"country": "Singapore",        "region": "Asia",           "gdp_nominal": 470,   "gdp_real": 360,   "population": 5.9,    "gdp_per_capita": 79661},
    {"country": "Bangladesh",       "region": "Asia",           "gdp_nominal": 450,   "gdp_real": 340,   "population": 170.0,  "gdp_per_capita": 2647},
    {"country": "Vietnam",          "region": "Asia",           "gdp_nominal": 430,   "gdp_real": 330,   "population": 97.3,   "gdp_per_capita": 4420},
    {"country": "Philippines",      "region": "Asia",           "gdp_nominal": 400,   "gdp_real": 320,   "population": 117.3,  "gdp_per_capita": 3411},
    {"country": "Malaysia",         "region": "Asia",           "gdp_nominal": 400,   "gdp_real": 330,   "population": 33.0,   "gdp_per_capita": 12121},
    {"country": "Hong Kong",        "region": "Asia",           "gdp_nominal": 360,   "gdp_real": 290,   "population": 7.4,    "gdp_per_capita": 48649},
    {"country": "Pakistan",         "region": "Asia",           "gdp_nominal": 340,   "gdp_real": 280,   "population": 231.4,  "gdp_per_capita": 1469},
    {"country": "Kazakhstan",       "region": "Asia",           "gdp_nominal": 260,   "gdp_real": 200,   "population": 19.4,   "gdp_per_capita": 13402},
    # Middle East
    {"country": "Saudi Arabia",     "region": "Middle East",    "gdp_nominal": 1100,  "gdp_real": 850,   "population": 36.4,   "gdp_per_capita": 30220},
    {"country": "Iran",             "region": "Middle East",    "gdp_nominal": 700,   "gdp_real": 600,   "population": 87.9,   "gdp_per_capita": 7963},
    {"country": "Israel",           "region": "Middle East",    "gdp_nominal": 520,   "gdp_real": 400,   "population": 9.7,    "gdp_per_capita": 53608},
    {"country": "UAE",              "region": "Middle East",    "gdp_nominal": 500,   "gdp_real": 400,   "population": 9.9,    "gdp_per_capita": 50505},
    # Oceania
    {"country": "Australia",        "region": "Oceania",        "gdp_nominal": 1690,  "gdp_real": 1350,  "population": 26.5,   "gdp_per_capita": 63773},
    {"country": "New Zealand",      "region": "Oceania",        "gdp_nominal": 250,   "gdp_real": 200,   "population": 5.1,    "gdp_per_capita": 49020},
    # Africa
    {"country": "Nigeria",          "region": "Africa",         "gdp_nominal": 360,   "gdp_real": 290,   "population": 223.8,  "gdp_per_capita": 1609},
    {"country": "South Africa",     "region": "Africa",         "gdp_nominal": 380,   "gdp_real": 340,   "population": 60.1,   "gdp_per_capita": 6323},
    {"country": "Egypt",            "region": "Africa",         "gdp_nominal": 380,   "gdp_real": 300,   "population": 104.3,  "gdp_per_capita": 3644},
    {"country": "Ethiopia",         "region": "Africa",         "gdp_nominal": 156,   "gdp_real": 130,   "population": 126.5,  "gdp_per_capita": 1233},
    {"country": "Morocco",          "region": "Africa",         "gdp_nominal": 140,   "gdp_real": 115,   "population": 37.5,   "gdp_per_capita": 3733},
    {"country": "Kenya",            "region": "Africa",         "gdp_nominal": 110,   "gdp_real": 88,    "population": 55.1,   "gdp_per_capita": 1996},
]


def get_dataframe() -> pd.DataFrame:
    """Return countries data as a pandas DataFrame."""
    return pd.DataFrame(COUNTRIES)
