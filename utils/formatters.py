"""Number formatting utilities for the GDP dashboard."""


def format_gdp(value_billions: float) -> str:
    """Format a GDP value (given in billions USD) with T/B/M suffix."""
    value = value_billions * 1_000_000_000
    abs_val = abs(value)
    sign = "-" if value < 0 else ""
    if abs_val >= 1e12:
        return f"{sign}${abs_val / 1e12:,.2f}T"
    if abs_val >= 1e9:
        return f"{sign}${abs_val / 1e9:,.2f}B"
    if abs_val >= 1e6:
        return f"{sign}${abs_val / 1e6:,.2f}M"
    return f"{sign}${abs_val:,.0f}"


def format_per_capita(value: float) -> str:
    """Format a per-capita USD value."""
    return f"${value:,.0f}"


def format_population(value_millions: float) -> str:
    """Format a population value (given in millions)."""
    if value_millions >= 1_000:
        return f"{value_millions / 1_000:.2f}B"
    return f"{value_millions:.1f}M"


def short_label(value_billions: float) -> str:
    """Compact label for chart annotations (e.g. $27.4T)."""
    value = value_billions * 1_000_000_000
    abs_val = abs(value)
    sign = "-" if value < 0 else ""
    if abs_val >= 1e12:
        return f"{sign}${abs_val / 1e12:.1f}T"
    if abs_val >= 1e9:
        return f"{sign}${abs_val / 1e9:.0f}B"
    return f"{sign}${abs_val / 1e6:.0f}M"
