"""GDP per Capita tab — calculator, rankings, and bubble explorer."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data.countries import get_dataframe
from utils.calculations import calculate_per_capita, get_rank, top_percentile
from utils.formatters import format_gdp, format_per_capita, format_population, short_label

# ── colours ───────────────────────────────────────────────────────────────────
REGION_COLORS = px.colors.qualitative.Plotly
ACCENT        = "#E63946"
PRIMARY       = "#457B9D"
CHART_BG      = "rgba(0,0,0,0)"
PLOT_LAYOUT   = dict(
    plot_bgcolor=CHART_BG,
    paper_bgcolor=CHART_BG,
    font=dict(family="Inter, sans-serif", size=13),
    margin=dict(t=50, b=30, l=10, r=10),
)


def _pc_comparison_bar(df: pd.DataFrame, user_pc: float, user_name: str) -> go.Figure:
    top20 = df.nlargest(20, "gdp_per_capita")[["country", "gdp_per_capita", "region"]].copy()
    if user_name not in top20["country"].values:
        user_row = pd.DataFrame([{"country": user_name, "gdp_per_capita": user_pc, "region": "Custom"}])
        top20 = pd.concat([top20, user_row], ignore_index=True)

    display = top20.sort_values("gdp_per_capita", ascending=True)
    colors  = [ACCENT if c == user_name else PRIMARY for c in display["country"]]

    fig = go.Figure(go.Bar(
        x=display["gdp_per_capita"],
        y=display["country"],
        orientation="h",
        marker_color=colors,
        text=display["gdp_per_capita"].apply(lambda v: f"${v:,.0f}"),
        textposition="auto",
        hovertemplate="<b>%{y}</b><br>GDP per Capita: $%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        title="GDP per Capita — Your Result vs Top 20",
        xaxis_title="GDP per Capita (USD)",
        height=max(520, len(display) * 24),
        **PLOT_LAYOUT,
        margin=dict(t=50, b=30, l=10, r=100),
    )
    return fig


def _world_pc_bar(df: pd.DataFrame, top_n: int, region: str) -> go.Figure:
    filtered = df if region == "All Regions" else df[df["region"] == region]
    display  = filtered.nlargest(top_n, "gdp_per_capita").sort_values("gdp_per_capita", ascending=True)

    fig = px.bar(
        display,
        x="gdp_per_capita", y="country",
        color="region",
        orientation="h",
        title=f"Top {top_n} Countries — GDP per Capita",
        labels={"gdp_per_capita": "GDP per Capita (USD)", "country": ""},
        text=display["gdp_per_capita"].apply(lambda v: f"${v:,.0f}"),
        color_discrete_sequence=REGION_COLORS,
        height=max(420, top_n * 26),
        hover_data={"population": True},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(**PLOT_LAYOUT, margin=dict(t=50, b=30, l=10, r=110))
    return fig


def _bubble_scatter(df: pd.DataFrame, gdp_col: str, gdp_label: str, log_x: bool, region: str) -> go.Figure:
    filtered = df if region == "All Regions" else df[df["region"] == region]

    fig = px.scatter(
        filtered,
        x=gdp_col,
        y="gdp_per_capita",
        size="population",
        color="region",
        hover_name="country",
        log_x=log_x,
        size_max=65,
        title=f"Total GDP vs GDP per Capita  (bubble = population)",
        labels={
            gdp_col:          f"{gdp_label} (Billions USD{'  · log scale' if log_x else ''})",
            "gdp_per_capita": "GDP per Capita (USD)",
            "population":     "Population (M)",
        },
        color_discrete_sequence=REGION_COLORS,
        height=520,
    )
    fig.update_traces(
        marker=dict(opacity=0.75, line=dict(width=1, color="white")),
        selector=dict(mode="markers"),
    )
    fig.update_layout(**PLOT_LAYOUT)
    return fig


# ── main render function ──────────────────────────────────────────────────────

def render_per_capita_tab(use_real: bool = False) -> None:
    df        = get_dataframe()
    gdp_col   = "gdp_real" if use_real else "gdp_nominal"
    gdp_label = "Real GDP (2015 USD)" if use_real else "Nominal GDP"

    # ── Section 1 — Calculator ──────────────────────────────────────────────
    st.markdown("### 🧮 GDP per Capita Calculator")
    st.markdown("Compare a country (or your own figures) against the world.")

    mode = st.radio(
        "Input Mode",
        ["Manual Input", "Select a Country"],
        horizontal=True,
        key="pc_mode",
    )

    user_pc    = None
    user_name  = "★ Your Country"

    if mode == "Manual Input":
        mc1, mc2 = st.columns(2)
        with mc1:
            user_gdp_bn = st.number_input(
                "Total GDP ($B)", min_value=0.0, value=0.0, step=50.0, key="pc_gdp_in",
                help="Enter the total GDP in billions of USD"
            )
        with mc2:
            user_pop_mn = st.number_input(
                "Population (Millions)", min_value=0.0, value=0.0, step=1.0, key="pc_pop_in",
                help="Enter the total population in millions"
            )
        if user_gdp_bn > 0 and user_pop_mn > 0:
            user_pc = calculate_per_capita(user_gdp_bn, user_pop_mn)

    else:
        country_list = sorted(df["country"].tolist())
        sel_country  = st.selectbox("Select a Country", country_list, key="pc_country_sel")
        row          = df[df["country"] == sel_country].iloc[0]
        user_gdp_bn  = row[gdp_col]
        user_pop_mn  = row["population"]
        user_pc      = row["gdp_per_capita"]
        user_name    = sel_country

        # Show the country's own stats
        info1, info2, info3 = st.columns(3)
        with info1:
            st.metric(f"{gdp_label}", format_gdp(row[gdp_col]))
        with info2:
            st.metric("Population", format_population(row["population"]))
        with info3:
            st.metric("Region", row["region"])

    # ── Results ─────────────────────────────────────────────────────────────
    if user_pc and user_pc > 0:
        rank      = get_rank(user_pc, df["gdp_per_capita"])
        total_n   = len(df)
        pct       = top_percentile(rank, total_n)
        world_avg = df["gdp_per_capita"].mean()
        diff_pct  = (user_pc - world_avg) / world_avg * 100

        st.markdown("---")
        st.markdown(f"#### 💰 Per Capita Results — *{user_name}*")

        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.metric("GDP per Capita", format_per_capita(user_pc))
        with r2:
            st.metric("Global Rank", f"#{rank} of {total_n}")
        with r3:
            st.metric("Top Percentile", f"{pct:.0f}%")
        with r4:
            delta_str = f"{diff_pct:+.1f}% vs avg"
            st.metric("World Average", format_per_capita(world_avg), delta_str)

        st.plotly_chart(_pc_comparison_bar(df, user_pc, user_name), use_container_width=True)

    # ── Section 2 — World Explorer ──────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🌍 World GDP per Capita Explorer")

    # Bubble chart
    bc1, bc2 = st.columns([4, 1])
    with bc2:
        st.markdown("**Bubble Chart Options**")
        regions_b  = ["All Regions"] + sorted(df["region"].unique())
        sel_reg_b  = st.selectbox("Region", regions_b, key="pc_bubble_region")
        log_x      = st.checkbox("Log Scale (X axis)", value=True, key="pc_log_x")
    with bc1:
        st.plotly_chart(
            _bubble_scatter(df, gdp_col, gdp_label, log_x, sel_reg_b),
            use_container_width=True,
        )

    st.caption(
        "Each bubble is a country. Bubble **size** represents population. "
        "Hover for details. Nations with large populations and low per-capita GDP "
        "cluster in the bottom-right; wealthy small nations in the top-left."
    )

    # Bar chart
    st.markdown("---")
    bc3, bc4 = st.columns([2, 2])
    with bc3:
        regions_pc = ["All Regions"] + sorted(df["region"].unique())
        sel_reg_pc = st.selectbox("Region", regions_pc, key="pc_bar_region")
    with bc4:
        top_n_pc = st.slider("Show top N", 5, len(df), 20, key="pc_topn")

    st.plotly_chart(_world_pc_bar(df, top_n_pc, sel_reg_pc), use_container_width=True)

    # Data table
    with st.expander("📋 Full Per Capita Data Table"):
        tbl = df.sort_values("gdp_per_capita", ascending=False)[
            ["country", "region", "gdp_per_capita", gdp_col, "population"]
        ].copy()
        tbl["gdp_per_capita"] = tbl["gdp_per_capita"].apply(format_per_capita)
        tbl[gdp_col]          = tbl[gdp_col].apply(format_gdp)
        tbl["population"]     = tbl["population"].apply(format_population)
        tbl.columns = ["Country", "Region", "GDP per Capita", gdp_label, "Population"]
        tbl = tbl.reset_index(drop=True)
        tbl.index = tbl.index + 1
        st.dataframe(tbl, use_container_width=True)

    # ── Reference ────────────────────────────────────────────────────────────
    with st.expander("📖 About GDP per Capita"):
        st.markdown("""
**GDP per Capita** divides a country's total economic output by its population:

$$\\text{GDP per Capita} = \\frac{\\text{GDP}}{\\text{Population}}$$

It is a widely-used proxy for **average living standards**, though it has limitations:
- It does not capture *income inequality* within a country.
- It ignores non-market production (household work, subsistence farming).
- Purchasing Power Parity (PPP) adjustments can give a more accurate welfare comparison.

**Interpretation guide:**

| Range | Rough Category |
|-------|---------------|
| > $50,000 | High-income (developed) |
| $15,000 – $50,000 | Upper-middle income |
| $4,000 – $15,000 | Lower-middle income |
| < $4,000 | Low-income |

*Source: World Bank income classifications (approximate).*
        """)
