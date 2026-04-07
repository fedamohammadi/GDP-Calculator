"""GDP Calculator & Explorer tab."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data.countries import get_dataframe
from utils.calculations import calculate_gdp, component_shares, get_rank, top_percentile
from utils.formatters import format_gdp, format_per_capita, format_population, short_label

# ── colour palette ────────────────────────────────────────────────────────────
REGION_COLORS = px.colors.qualitative.Plotly
ACCENT        = "#E63946"   # red highlight for "your economy"
PRIMARY       = "#457B9D"
CHART_BG      = "rgba(0,0,0,0)"

PLOT_LAYOUT = dict(
    plot_bgcolor=CHART_BG,
    paper_bgcolor=CHART_BG,
    font=dict(family="Inter, sans-serif", size=13),
    margin=dict(t=50, b=30, l=10, r=10),
)


def _waterfall(c, i, g, nx, total):
    labels = ["Consumption (C)", "Investment (I)", "Government (G)", "Net Exports (NX)", "Total GDP"]
    values = [c, i, g, nx, total]
    measures = ["relative", "relative", "relative", "relative", "total"]

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=measures,
        x=labels,
        y=values,
        text=[short_label(v) for v in values],
        textposition="outside",
        decreasing={"marker": {"color": "#E63946", "line": {"color": "#E63946", "width": 1}}},
        increasing={"marker": {"color": "#2DC653", "line": {"color": "#2DC653", "width": 1}}},
        totals={"marker":    {"color": PRIMARY,    "line": {"color": PRIMARY,    "width": 1}}},
        connector={"line":   {"color": "#CCC", "dash": "dot", "width": 1}},
    ))
    fig.update_layout(
        title="GDP Component Breakdown (Waterfall)",
        yaxis_title="GDP (Billions USD)",
        height=360,
        **PLOT_LAYOUT,
    )
    return fig


def _comparison_bar(df: pd.DataFrame, user_gdp: float, gdp_col: str, gdp_label: str):
    top20 = df.nlargest(20, gdp_col)[["country", gdp_col, "region"]].copy()
    user_row = pd.DataFrame([{"country": "★ Your Economy", gdp_col: user_gdp, "region": "Custom"}])
    combined = pd.concat([top20, user_row], ignore_index=True).sort_values(gdp_col, ascending=True)

    colors = [ACCENT if c == "★ Your Economy" else PRIMARY for c in combined["country"]]

    fig = go.Figure(go.Bar(
        x=combined[gdp_col],
        y=combined["country"],
        orientation="h",
        marker_color=colors,
        text=combined[gdp_col].apply(short_label),
        textposition="auto",
        hovertemplate="<b>%{y}</b><br>GDP: %{x:.0f}B USD<extra></extra>",
    ))
    fig.update_layout(
        title=f"Your Economy vs Top 20 — {gdp_label}",
        xaxis_title="GDP (Billions USD)",
        height=max(480, len(combined) * 22),
        **PLOT_LAYOUT,
        margin=dict(t=50, b=30, l=10, r=80),
    )
    return fig


def _world_bar(df: pd.DataFrame, gdp_col: str, gdp_label: str, top_n: int, region: str, ascending: bool):
    filtered = df if region == "All Regions" else df[df["region"] == region]
    display  = filtered.nlargest(top_n, gdp_col).sort_values(gdp_col, ascending=ascending)

    fig = px.bar(
        display,
        x=gdp_col, y="country",
        color="region",
        orientation="h",
        title=f"Top {top_n} Economies — {gdp_label}",
        labels={gdp_col: "GDP (Billions USD)", "country": ""},
        text=display[gdp_col].apply(short_label),
        color_discrete_sequence=REGION_COLORS,
        height=max(420, top_n * 26),
        hover_data={"population": True, "gdp_per_capita": True},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(**PLOT_LAYOUT, margin=dict(t=50, b=30, l=10, r=90))
    return fig, display


# ── main render function ──────────────────────────────────────────────────────

def render_gdp_tab(use_real: bool = False) -> None:
    df        = get_dataframe()
    gdp_col   = "gdp_real" if use_real else "gdp_nominal"
    gdp_label = "Real GDP (2015 constant USD)" if use_real else "Nominal GDP"

    # ── Section 1 — Calculator ──────────────────────────────────────────────
    st.markdown("### 🧮 GDP Calculator")
    st.markdown(
        "Enter each expenditure component (in **billions USD**). "
        "Net Exports can be negative when a country imports more than it exports."
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        c  = st.number_input("Consumption (C) $B",      min_value=0.0,    value=0.0, step=50.0,
                             help="Total household & business spending on goods and services")
    with col2:
        i  = st.number_input("Investment (I) $B",        min_value=0.0,    value=0.0, step=50.0,
                             help="Business capital expenditure, residential construction, inventory")
    with col3:
        g  = st.number_input("Government (G) $B",        min_value=0.0,    value=0.0, step=50.0,
                             help="Government purchases of goods and services (excludes transfers)")
    with col4:
        nx = st.number_input("Net Exports (NX) $B",      value=0.0,        step=10.0,
                             help="Exports − Imports. Negative when trade deficit exists.")

    has_input = any(v != 0 for v in [c, i, g, nx])

    if has_input:
        total_gdp = calculate_gdp(c, i, g, nx)
        rank      = get_rank(total_gdp, df[gdp_col])
        total_n   = len(df)
        pct       = top_percentile(rank, total_n)

        st.markdown("---")
        st.markdown("#### 📊 Results")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total GDP", format_gdp(total_gdp))
        with m2:
            st.metric("Global Rank", f"#{rank} of {total_n}")
        with m3:
            st.metric("Top Percentile", f"{pct:.1f}%")
        with m4:
            comps = {"C": c, "I": i, "G": g, "NX": nx}
            dom_key = max(comps, key=lambda k: abs(comps[k]))
            dom_share = abs(comps[dom_key]) / abs(total_gdp) * 100 if total_gdp else 0
            st.metric("Largest Component", f"{dom_key}  ({dom_share:.0f}%)")

        chart_l, chart_r = st.columns([1, 1])
        with chart_l:
            st.plotly_chart(_waterfall(c, i, g, nx, total_gdp), use_container_width=True)
        with chart_r:
            st.plotly_chart(_comparison_bar(df, total_gdp, gdp_col, gdp_label), use_container_width=True)

        # ── inline explainer ───────────────────────────────────────────────
        with st.expander("📚 What do these numbers mean?"):
            shares = component_shares(c, i, g, nx)
            lines  = [f"- **{k}**: {v:+.1f}% of GDP" for k, v in shares.items()]
            st.markdown("\n".join(lines))
            world_avg = df[gdp_col].mean()
            st.markdown(
                f"\nThe **world average** {gdp_label} across our dataset is "
                f"**{format_gdp(world_avg)}**.  \n"
                f"Your calculated economy is "
                f"**{'above' if total_gdp > world_avg else 'below'}** that average "
                f"by **{abs(total_gdp - world_avg):,.0f}B**."
            )

    # ── Section 2 — World Rankings ──────────────────────────────────────────
    st.markdown("---")
    st.markdown(f"### 🌍 World {gdp_label} Rankings")
    st.caption("Data: IMF/World Bank estimates, 2023  ·  56 economies")

    fc1, fc2, fc3 = st.columns([2, 2, 1])
    with fc1:
        regions = ["All Regions"] + sorted(df["region"].unique())
        sel_region = st.selectbox("Region", regions, key="gdp_region")
    with fc2:
        top_n = st.slider("Show top N countries", 5, len(df), 20, key="gdp_topn")
    with fc3:
        ascending = st.checkbox("Ascending", False, key="gdp_asc")

    fig_world, display_df = _world_bar(df, gdp_col, gdp_label, top_n, sel_region, ascending)
    st.plotly_chart(fig_world, use_container_width=True)

    with st.expander("📋 Data Table"):
        tbl = display_df[["country", "region", gdp_col, "gdp_per_capita", "population"]].copy()
        tbl[gdp_col]         = tbl[gdp_col].apply(format_gdp)
        tbl["gdp_per_capita"] = tbl["gdp_per_capita"].apply(format_per_capita)
        tbl["population"]     = tbl["population"].apply(format_population)
        tbl.columns = ["Country", "Region", gdp_label, "GDP per Capita", "Population"]
        tbl = tbl.reset_index(drop=True)
        tbl.index = tbl.index + 1
        st.dataframe(tbl, use_container_width=True)

    # ── Section 3 — GDP Formula Reference ───────────────────────────────────
    with st.expander("📖 GDP Formula Reference"):
        st.markdown("""
**Expenditure Approach**
$$GDP = C + I + G + NX$$

| Symbol | Component | Description |
|--------|-----------|-------------|
| **C** | Consumption | Household spending on goods & services |
| **I** | Investment | Business capital, housing, inventories |
| **G** | Government | Public sector purchases (not transfers) |
| **NX** | Net Exports | Exports − Imports |

**Nominal vs Real GDP**
- **Nominal GDP** is measured at current market prices. It rises with both real growth *and* inflation.
- **Real GDP** is adjusted for inflation using a base-year price level (here: 2015 USD), isolating genuine output growth.
        """)
