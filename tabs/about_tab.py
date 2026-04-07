"""About tab — friendly, visual guide to GDP concepts."""

import plotly.graph_objects as go
import streamlit as st

# ── shared palette ────────────────────────────────────────────────────────────
PRIMARY   = "#1d375d"
ACCENT    = "#E63946"
GREEN     = "#2DC653"
AMBER     = "#F4A261"
CHART_BG  = "rgba(0,0,0,0)"
PLOT_BASE = dict(
    plot_bgcolor=CHART_BG,
    paper_bgcolor=CHART_BG,
    font=dict(family="Inter, sans-serif", size=13, color="#111111"),
    margin=dict(t=40, b=40, l=20, r=20),
)

# ── tiny helpers ──────────────────────────────────────────────────────────────

def _card(icon, title, body, accent_color=PRIMARY):
    return f"""
    <div style="
        background:#FFFFFF;
        border:1px solid #E0DDD6;
        border-top:4px solid {accent_color};
        border-radius:10px;
        padding:1.2rem 1.1rem 1rem 1.1rem;
        height:100%;
    ">
        <div style="font-size:1.8rem;margin-bottom:.4rem">{icon}</div>
        <div style="font-weight:600;font-size:.95rem;color:#111111;margin-bottom:.4rem">{title}</div>
        <div style="font-size:.85rem;color:#444444;line-height:1.6">{body}</div>
    </div>"""


def _pill(label, color=PRIMARY):
    return (
        f'<span style="background:{color};color:#fff;'
        f'border-radius:20px;padding:.18rem .7rem;'
        f'font-size:.78rem;font-weight:600;margin-right:.3rem">{label}</span>'
    )


def _section_header(title, subtitle=""):
    sub = f'<p style="color:#666;font-size:.88rem;margin:.3rem 0 0 0">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f"""<div style="border-left:4px solid {PRIMARY};padding-left:.9rem;margin:1.6rem 0 1rem 0">
        <h3 style="margin:0;color:#111111;font-size:1.1rem">{title}</h3>{sub}</div>""",
        unsafe_allow_html=True,
    )


# ── waterfall: C + I + G + NX = GDP ──────────────────────────────────────────

def _formula_chart():
    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "total"],
        x=["Consumption (C)", "Investment (I)", "Government (G)", "Net Exports (NX)", "Total GDP"],
        y=[14_000, 4_000, 4_500, -900, 0],
        text=["$14 T", "$4 T", "$4.5 T", "−$0.9 T", "$21.6 T"],
        textposition="outside",
        decreasing={"marker": {"color": ACCENT}},
        increasing={"marker": {"color": "#457B9D"}},
        totals={"marker":    {"color": PRIMARY}},
        connector={"line":   {"color": "#CCC", "dash": "dot", "width": 1}},
    ))
    fig.update_layout(
        title="Example: How the US GDP adds up (~2023)",
        yaxis_title="Billions USD",
        height=340,
        **PLOT_BASE,
    )
    return fig


# ── nominal vs real line chart ────────────────────────────────────────────────

def _nominal_vs_real_chart():
    years   = list(range(2000, 2024))
    nominal = [10_290, 10_621, 10_977, 11_510, 12_274, 13_093, 13_855, 14_477,
               14_718, 14_419, 15_049, 15_599, 16_254, 16_844, 17_527, 18_225,
               18_715, 19_519, 20_580, 21_433, 23_315, 25_463, 25_744, 27_360]
    real    = [13_131, 13_263, 13_493, 13_879, 14_406, 14_913, 15_338, 15_626,
               15_605, 15_209, 15_599, 15_840, 16_197, 16_495, 16_912, 17_404,
               17_689, 18_108, 18_638, 19_073, 19_548, 20_317, 20_014, 20_990]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=nominal, name="Nominal GDP",
        line=dict(color=ACCENT, width=2.5),
        hovertemplate="<b>%{x}</b><br>Nominal: $%{y:,}B<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=years, y=real, name="Real GDP (2015 USD)",
        line=dict(color=PRIMARY, width=2.5, dash="dash"),
        hovertemplate="<b>%{x}</b><br>Real: $%{y:,}B<extra></extra>",
    ))
    fig.add_vrect(
        x0=2008, x1=2009,
        fillcolor="rgba(230,57,70,0.1)", line_width=0,
        annotation_text="2008 Crisis", annotation_position="top left",
        annotation_font_size=11, annotation_font_color="#666",
    )
    fig.add_vrect(
        x0=2020, x1=2021,
        fillcolor="rgba(244,162,97,0.15)", line_width=0,
        annotation_text="COVID-19", annotation_position="top left",
        annotation_font_size=11, annotation_font_color="#666",
    )
    fig.update_layout(
        title="Nominal vs Real GDP — USA (2000–2023, approx.)",
        yaxis_title="Billions USD",
        height=340,
        xaxis=dict(tickcolor="#111111", linecolor="#CCC", gridcolor="#E8E4DD", color="#111111"),
        yaxis=dict(tickcolor="#111111", linecolor="#CCC", gridcolor="#E8E4DD", color="#111111"),
        legend=dict(font=dict(color="#111111"), bgcolor="rgba(0,0,0,0)"),
        **PLOT_BASE,
    )
    return fig


# ── per-capita bar ────────────────────────────────────────────────────────────

def _per_capita_bar():
    countries = ["Norway", "Switzerland", "USA", "Germany", "China", "India", "Nigeria"]
    gdp_pc    = [106_000, 93_000, 76_000, 51_000, 12_600, 2_400, 2_200]
    colors    = [PRIMARY if c != "USA" else ACCENT for c in countries]

    fig = go.Figure(go.Bar(
        x=gdp_pc,
        y=countries,
        orientation="h",
        marker_color=colors,
        text=[f"${v:,}" for v in gdp_pc],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>$%{x:,} per person<extra></extra>",
    ))
    fig.update_layout(
        title="GDP per Capita — selected countries (approx. 2023)",
        xaxis_title="USD per person",
        height=320,
        xaxis=dict(tickcolor="#111111", linecolor="#CCC", gridcolor="#E8E4DD", color="#111111"),
        yaxis=dict(tickcolor="#111111", linecolor="#CCC", gridcolor="#E8E4DD", color="#111111"),
        **PLOT_BASE,
    )
    return fig


# ── GDP size vs wealth scatter ────────────────────────────────────────────────

def _size_vs_wealth():
    names  = ["USA", "China", "Germany", "India", "Norway", "Nigeria", "Switzerland", "Japan"]
    gdp    = [27000, 17700, 4400, 3700, 580, 477, 870, 4200]
    gdppc  = [76000, 12600, 51000, 2400, 106000, 2200, 93000, 33800]
    pop    = [335, 1410, 84, 1430, 5.5, 220, 8.8, 124]
    colors = [ACCENT, PRIMARY, "#457B9D", "#F4A261", "#2DC653", "#E9C46A", "#2DC653", "#264653"]

    fig = go.Figure()
    for n, x, y, s, c in zip(names, gdp, gdppc, pop, colors):
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode="markers+text",
            name=n,
            text=[n],
            textposition="top center",
            marker=dict(size=max(12, s ** 0.45 * 4), color=c, opacity=0.85,
                        line=dict(width=1, color="white")),
            hovertemplate=f"<b>{n}</b><br>Total GDP: ${x:,}B<br>Per Capita: ${y:,}<extra></extra>",
            showlegend=False,
        ))
    fig.update_layout(
        title="Big economy ≠ rich citizens  (bubble size ≈ population)",
        xaxis_title="Total GDP (Billions USD)",
        yaxis_title="GDP per Capita (USD)",
        height=380,
        xaxis=dict(tickcolor="#111111", linecolor="#CCC", gridcolor="#E8E4DD", color="#111111"),
        yaxis=dict(tickcolor="#111111", linecolor="#CCC", gridcolor="#E8E4DD", color="#111111"),
        **PLOT_BASE,
    )
    return fig


# ── main render ───────────────────────────────────────────────────────────────

def render_about_tab() -> None:

    # ── Hero ─────────────────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {PRIMARY} 0%, #2a4f80 100%);
            border-radius: 12px;
            padding: 2.2rem 2rem 1.8rem 2rem;
            margin-bottom: 1.5rem;
            color: #fff;
        ">
            <div style="font-size:2.4rem;margin-bottom:.5rem">📘</div>
            <div style="margin:0 0 .5rem 0;font-size:1.6rem;color:#fff;font-weight:700;font-family:Inter,sans-serif">
                Your Quick Guide to GDP
            </div>
            <p style="margin:0;font-size:.95rem;color:rgba(255,255,255,.85);line-height:1.7;max-width:640px">
                Before diving into the numbers, here's everything you need to know —
                explained simply, without jargon. Read through once and the whole
                dashboard will make perfect sense.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Quick-pick navigation ─────────────────────────────────────────────────
    st.markdown(
        "<p style='font-size:.82rem;color:#888;margin-bottom:.5rem'>Jump to a topic:</p>",
        unsafe_allow_html=True,
    )
    pills_html = (
        _pill("What is GDP?", PRIMARY)
        + _pill("The GDP Formula", "#457B9D")
        + _pill("Nominal vs Real", ACCENT)
        + _pill("GDP per Capita", "#2DC653")
        + _pill("Limitations", AMBER)
        + _pill("Key Terms", "#6c757d")
    )
    st.markdown(pills_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # 1 · WHAT IS GDP?
    # ═══════════════════════════════════════════════════════════════════════════
    _section_header("What is GDP?", "The single number that tries to measure an entire economy")

    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown(
            """
            **GDP** stands for **Gross Domestic Product**. It's the total value
            of all goods and services produced inside a country in one year.

            Think of it as the country's "annual report" — one number that captures
            how much economic activity happened.

            - A bakery sells bread → that's in the GDP.
            - A factory builds cars → that's in the GDP.
            - The government builds a road → that's in the GDP too.

            If the GDP goes up, the economy grew. If it falls, the economy shrank.
            Two quarters of shrinking GDP in a row is called a **recession**.
            """
        )
    with col_b:
        st.markdown(
            f"""
            <div style="background:#FFFFFF;border:1px solid #E0DDD6;border-radius:10px;
                        padding:1.4rem;text-align:center">
                <div style="font-size:.8rem;color:#888;text-transform:uppercase;
                            letter-spacing:.8px;margin-bottom:.4rem">World GDP (2023 est.)</div>
                <div style="font-size:2.2rem;font-weight:700;color:{PRIMARY}">$105 T</div>
                <div style="font-size:.82rem;color:#666;margin-top:.3rem">
                    That's $105,000,000,000,000 — <br>roughly $13,000 per person on Earth.
                </div>
                <hr style="border-color:#eee;margin:.9rem 0">
                <div style="font-size:.8rem;color:#888;text-transform:uppercase;
                            letter-spacing:.8px;margin-bottom:.4rem">Largest economy</div>
                <div style="font-size:1.5rem;font-weight:700;color:{ACCENT}">🇺🇸 USA</div>
                <div style="font-size:.82rem;color:#666">~$27 trillion · ~26% of world GDP</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # 2 · THE GDP FORMULA
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    _section_header("The GDP Formula", "Four building blocks that add up to the full picture")

    st.markdown(
        f"""
        <div style="background:{PRIMARY};color:#fff;border-radius:10px;
                    padding:1rem 1.5rem;text-align:center;font-size:1.3rem;
                    font-weight:700;letter-spacing:.5px;margin-bottom:1.2rem">
            GDP &nbsp;=&nbsp; C &nbsp;+&nbsp; I &nbsp;+&nbsp; G &nbsp;+&nbsp; NX
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        ("🛒", "C — Consumption", "Everything households spend: groceries, phones, rent, Netflix. "
         "Usually the biggest slice — around <b>60–70%</b> of GDP in most countries.", "#457B9D"),
        ("🏗️", "I — Investment", "Money businesses spend on equipment, buildings, and software — "
         "plus new homes. Not stocks or bonds! Those are just transfers of ownership.", "#2DC653"),
        ("🏛️", "G — Government", "What the government buys: schools, hospitals, defence, roads. "
         "It <em>excludes</em> welfare payments — those are transfers, not purchases.", PRIMARY),
        ("🚢", "NX — Net Exports", "Exports <em>minus</em> imports. If a country sells more than it "
         "buys from abroad, NX is positive. A trade deficit makes NX negative.", ACCENT),
    ]
    for col, (icon, title, body, color) in zip([c1, c2, c3, c4], cards):
        with col:
            st.markdown(_card(icon, title, body, color), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("📊 See it in action — US GDP breakdown (interactive chart)"):
        st.plotly_chart(_formula_chart(), use_container_width=True)
        st.caption(
            "Hover over each bar. Notice how NX is negative — the US imports more than it exports. "
            "Consumption dominates, as it does in most large economies."
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # 3 · NOMINAL vs REAL
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    _section_header("Nominal vs Real GDP", "Why the same economy can look different depending on how you measure it")

    col_nom, col_real = st.columns(2)
    with col_nom:
        st.markdown(
            f"""
            <div style="background:#FFFFFF;border:1px solid #E0DDD6;border-top:4px solid {ACCENT};
                        border-radius:10px;padding:1.2rem">
                <div style="font-size:1.4rem">💵</div>
                <div style="font-weight:700;font-size:.98rem;margin:.3rem 0">Nominal GDP</div>
                <div style="font-size:.86rem;color:#444;line-height:1.65">
                    Measured at <b>today's prices</b>. Easy to calculate, but can be
                    misleading — if prices rise 5% and production doesn't change at all,
                    Nominal GDP still rises 5%. You haven't actually made more stuff.
                    <br><br>
                    <b>Good for:</b> comparing country sizes in the same year.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_real:
        st.markdown(
            f"""
            <div style="background:#FFFFFF;border:1px solid #E0DDD6;border-top:4px solid {PRIMARY};
                        border-radius:10px;padding:1.2rem">
                <div style="font-size:1.4rem">📏</div>
                <div style="font-weight:700;font-size:.98rem;margin:.3rem 0">Real GDP</div>
                <div style="font-size:.86rem;color:#444;line-height:1.65">
                    Adjusted for <b>inflation</b> using a fixed base year (here: 2015).
                    Shows genuine changes in how much an economy actually produces,
                    stripping out the effect of rising prices.
                    <br><br>
                    <b>Good for:</b> tracking growth over time, spotting recessions.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("📈 See the difference — Nominal vs Real on a chart (interactive)"):
        st.plotly_chart(_nominal_vs_real_chart(), use_container_width=True)
        st.caption(
            "Notice how Nominal GDP (red) always looks higher and grows faster than Real GDP (blue dashed). "
            "That gap is inflation. During 2020–2021 you can see Real GDP dip and recover — "
            "that reflects actual production loss from COVID, while Nominal rose partly due to price surges."
        )

    st.info(
        "**Quick check:** If a country's GDP rose 8% but inflation was 6%, "
        "how much did the economy actually grow?  \n"
        "→ About **2%** in real terms. That's what matters for people's lives."
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # 4 · GDP PER CAPITA
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    _section_header("GDP per Capita", "Big economy vs. rich citizens — they're not the same thing")

    st.markdown(
        """
        **GDP per capita** simply divides a country's total GDP by its population.
        It's the closest thing we have to a single number for *average living standards*.

        **Why does it matter?** China has a larger total GDP than Switzerland, but
        Switzerland has over 7× the GDP per capita — meaning the *average Swiss person*
        is far wealthier than the average Chinese person (by this measure).
        """
    )

    st.latex(r"\text{GDP per Capita} = \frac{\text{Total GDP}}{\text{Population}}")

    with st.expander("🌍 Compare countries — GDP per Capita chart (interactive)"):
        st.plotly_chart(_per_capita_bar(), use_container_width=True)
        st.caption("Hover for exact values. Notice Norway and Switzerland at the top despite being small countries.")

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("🔵 Big economy vs rich citizens — scatter plot (interactive)"):
        st.plotly_chart(_size_vs_wealth(), use_container_width=True)
        st.caption(
            "India and China have huge total GDPs but low per-capita wealth. "
            "Norway and Switzerland are the opposite — small economies, very high living standards."
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # 5 · LIMITATIONS
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    _section_header("What GDP Doesn't Tell You", "Every useful tool has blind spots — here are GDP's")

    lim_cols = st.columns(3)
    limitations = [
        ("⚖️", "Inequality", "GDP per capita is an average. A country where 10 people "
         "earn $1M and 990 earn $1,000 has the same 'average' as one where everyone "
         "earns $10,900. GDP doesn't see the difference.", AMBER),
        ("🌿", "Environment", "Clear-cutting a forest boosts GDP (timber sold). "
         "Cleaning up a polluted river costs GDP (spending without new production). "
         "GDP treats environmental damage as a neutral or positive.", ACCENT),
        ("🏠", "Unpaid work", "A parent raising children, a person cooking at home, "
         "volunteers — none of this counts. But hire a nanny or order takeout, "
         "and suddenly it's in the GDP.", "#6c757d"),
    ]
    for col, (icon, title, body, color) in zip(lim_cols, limitations):
        with col:
            st.markdown(_card(icon, title, body, color), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        > **Bottom line:** GDP is a powerful tool for measuring economic size and growth,
        > but it's not a measure of happiness, sustainability, or fairness.
        > Economists often use it alongside other indicators like the Human Development Index (HDI),
        > Gini coefficient, and median household income.
        """
    )

    # ═══════════════════════════════════════════════════════════════════════════
    # 6 · KEY TERMS GLOSSARY
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("---")
    _section_header("Key Terms at a Glance", "A quick reference you can come back to anytime")

    terms = {
        "GDP (Gross Domestic Product)": "The total value of all goods and services produced within a country's borders in a year.",
        "Nominal GDP": "GDP measured at current prices. Useful for comparing economies in the same year.",
        "Real GDP": "GDP adjusted for inflation, using a fixed base year. Useful for tracking growth over time.",
        "GDP per Capita": "GDP divided by population — a rough proxy for average living standards.",
        "Expenditure Approach": "Calculating GDP by adding C + I + G + NX — the most common method.",
        "Inflation": "A general rise in prices over time. It inflates Nominal GDP without reflecting more production.",
        "Recession": "Two consecutive quarters of negative GDP growth.",
        "Trade Deficit": "When a country imports more than it exports — makes Net Exports (NX) negative.",
        "Base Year": "The fixed reference year used to calculate Real GDP (this dashboard uses 2015).",
        "HDI (Human Development Index)": "A broader measure of wellbeing that includes health and education alongside income.",
    }

    col_left, col_right = st.columns(2)
    items = list(terms.items())
    half = len(items) // 2 + len(items) % 2
    for col, chunk in zip([col_left, col_right], [items[:half], items[half:]]):
        with col:
            for term, defn in chunk:
                st.markdown(
                    f"""
                    <div style="border-left:3px solid {PRIMARY};padding:.5rem .8rem;
                                margin-bottom:.7rem;background:#FFFFFF;border-radius:0 6px 6px 0">
                        <div style="font-weight:600;font-size:.88rem;color:{PRIMARY}">{term}</div>
                        <div style="font-size:.83rem;color:#444;margin-top:.2rem;line-height:1.55">{defn}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ── Footer nudge ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        f"""
        <div style="text-align:center;padding:1.2rem;background:#FFFFFF;
                    border:1px solid #E0DDD6;border-radius:10px">
            <div style="font-size:1.5rem;margin-bottom:.4rem">🚀</div>
            <div style="font-weight:600;color:#111;font-size:.98rem">Ready to explore?</div>
            <div style="color:#666;font-size:.86rem;margin-top:.3rem">
                Head to the <b>GDP Calculator & Explorer</b> or <b>GDP per Capita</b> tabs
                and start playing with real data from 57 economies.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
