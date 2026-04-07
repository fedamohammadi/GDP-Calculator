"""
Global GDP Explorer — Streamlit Dashboard
==========================================
Entry point: streamlit run app.py
"""

from pathlib import Path

import streamlit as st

# ── Page config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="Global GDP Explorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "Global GDP Explorer · Built with Streamlit & Plotly"},
)

# ── Inject custom CSS ──────────────────────────────────────────────────────
css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# ── Import tab renderers (after st.set_page_config) ───────────────────────
from tabs.gdp_tab import render_gdp_tab
from tabs.per_capita_tab import render_per_capita_tab

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌍 GDP Explorer")
    st.markdown("---")

    st.markdown("### ⚙️ Settings")
    gdp_type = st.radio(
        "GDP Measure",
        ["Nominal GDP", "Real GDP (2015 USD)"],
        index=0,
        help=(
            "**Nominal GDP** uses current market prices.  \n"
            "**Real GDP** is inflation-adjusted to 2015 constant USD."
        ),
    )
    use_real = gdp_type == "Real GDP (2015 USD)"

    st.markdown("---")
    st.markdown("### 📌 About")
    st.markdown(
        """
        A platform for exploring, calculating, and comparing
        **GDP** and **GDP per Capita** across 56 world economies.

        **Data:** IMF / World Bank estimates, 2023.

        **Tabs:**
        - **GDP Calculator** — compute GDP from C+I+G+NX and compare globally
        - **GDP per Capita** — analyse living standards across nations

        *Future: World Bank live data & ML forecasting.*
        """
    )
    st.markdown("---")
    st.caption("Built with Streamlit & Plotly  ·  Feda Mohammadi")

# ── Hero header ────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="dashboard-header">
        <h1>🌍 Global GDP Explorer</h1>
        <p>Explore, calculate, and compare economic output across the world</p>
        <div class="badges">
            <span class="badge">📊 56 Economies</span>
            <span class="badge">🗂️ Nominal &amp; Real GDP</span>
            <span class="badge">👤 GDP per Capita</span>
            <span class="badge">📈 Interactive Charts</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Tabs ────────────────────────────────────────────────────────────────────
tab_gdp, tab_pc = st.tabs(["📈  GDP Calculator & Explorer", "👤  GDP per Capita"])

with tab_gdp:
    render_gdp_tab(use_real=use_real)

with tab_pc:
    render_per_capita_tab(use_real=use_real)
