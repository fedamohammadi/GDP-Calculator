"""Pure GDP calculation utilities."""

import pandas as pd


def calculate_gdp(c: float, i: float, g: float, nx: float) -> float:
    """Expenditure approach: GDP = C + I + G + NX (all in the same unit)."""
    return c + i + g + nx


def calculate_per_capita(gdp_billions: float, population_millions: float) -> float:
    """Return GDP per capita in USD from billion-dollar GDP and million-person population."""
    if population_millions <= 0:
        return 0.0
    return (gdp_billions * 1_000) / population_millions  # = (B / M) * 1000 → USD


def get_rank(value: float, series: pd.Series) -> int:
    """1-based rank (1 = highest) of *value* within *series*."""
    return int((series > value).sum()) + 1


def top_percentile(rank: int, total: int) -> float:
    """Return the top-N% figure (e.g. rank=1 → 100%, rank=total → ~0%)."""
    return ((total - rank + 1) / total) * 100


def component_shares(c: float, i: float, g: float, nx: float) -> dict:
    """Return each component's share of total GDP as a percentage."""
    total = calculate_gdp(c, i, g, nx)
    if total == 0:
        return {"Consumption (C)": 0, "Investment (I)": 0, "Government (G)": 0, "Net Exports (NX)": 0}
    return {
        "Consumption (C)":   round(c  / total * 100, 2),
        "Investment (I)":    round(i  / total * 100, 2),
        "Government (G)":    round(g  / total * 100, 2),
        "Net Exports (NX)":  round(nx / total * 100, 2),
    }
