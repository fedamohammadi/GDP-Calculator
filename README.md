# 🌍 Global GDP Dashboard

An interactive, browser-based dashboard for exploring, calculating, and comparing economic output across the world — no setup, no code required.
Enter GDP components, see your economy ranked globally, and build real intuition for how national income is measured.

**[▶ Open the live app](https://globalgdpapp-if4rjn5zrxsmgfaqktmnqc.streamlit.app/)**

---

## 💡 What is this?

Global GDP Dashboard is a self-contained learning and exploration tool that covers the fundamentals of macroeconomics through live, interactive visualisations. It lets you calculate GDP from scratch using the expenditure approach (C + I + G + NX), benchmark your result against 57 real economies, and explore how GDP per capita differs from raw economic size.

It is designed for students, educators, and anyone curious about economics who wants to go beyond textbook formulas and see real data come to life — no economics background required.

---

## 📖 What will I learn?

The **About** tab walks you through everything before you touch the data:

- What GDP actually measures — and what it doesn't
- The four components of the expenditure formula (C, I, G, NX)
- The difference between Nominal and Real GDP
- Why GDP per capita matters more than total GDP for comparing living standards
- The limitations of GDP as a measure of wellbeing
- A full glossary of key terms

Every concept is explained in plain, jargon-free language and paired with interactive charts.

---

## 🚀 What can I do?

### 📈 GDP Calculator & Explorer

A full GDP calculator built on the expenditure approach:

| Feature | What you can do |
|---------|-----------------|
| **GDP Calculator** | Enter Consumption (C), Investment (I), Government (G), and Net Exports (NX) in billions USD and compute total GDP instantly |
| **Global Ranking** | See where your calculated economy ranks among 57 real-world economies |
| **Top Percentile** | Find out what percentile your economy falls in globally |
| **Waterfall Chart** | Visualise how each component contributes to — or subtracts from — total GDP |
| **Comparison Bar Chart** | Plot your economy side-by-side against the top 20 countries in the dataset |
| **World Rankings** | Browse the full leaderboard, filter by region, adjust how many countries to show, and sort ascending or descending |
| **Data Table** | View the underlying figures for any filtered selection |
| **Toggle: Nominal / Real** | Switch between Nominal GDP and Real GDP (2015 constant USD) using the sidebar |

### 👤 GDP per Capita

Dig deeper into living standards:

| Feature | What you can do |
|---------|-----------------|
| **Manual Calculator** | Enter any GDP and population to compute GDP per capita and rank it globally |
| **Country Lookup** | Select any of the 57 countries to instantly pull its real data and see how it compares |
| **Per Capita Ranking** | See your result ranked against the world, with world-average comparison and delta |
| **Comparison Bar Chart** | See your selected country or custom input plotted against the top 20 |
| **Bubble Scatter Chart** | Explore total GDP vs per capita wealth, with bubble size representing population |
| **World Per Capita Bar** | Filter by region and browse the top-N countries by per capita income |
| **Data Table** | Full sortable table of all 57 economies |

### 📘 About

An interactive, visual explainer covering everything you need to know before exploring the data — GDP, the formula, Nominal vs Real, per capita, limitations, and a full glossary.

---

## 🗂 Project structure

```
🌍 global_gdp_app/
│
├── 📄 app.py                    # Entry point — page config, sidebar, tab layout
│
├── 📁 tabs/
│   ├── 📄 about_tab.py          # Interactive GDP education guide
│   ├── 📄 gdp_tab.py            # GDP Calculator & World Rankings tab
│   └── 📄 per_capita_tab.py     # GDP per Capita tab
│
├── 📁 data/
│   └── 📄 countries.py          # Dataset — 57 economies, IMF/World Bank 2023
│
├── 📁 utils/
│   ├── 📄 calculations.py       # GDP formula, ranking, percentile, per capita logic
│   └── 📄 formatters.py         # Number and label formatting helpers
│
├── 📁 assets/
│   └── 🎨 style.css             # Custom theme — warm cream palette, navy sidebar
│
├── 📁 .streamlit/
│   └── ⚙️  config.toml          # Light theme configuration
│
└── 📄 requirements.txt
```

---

## 🛠️ Tech stack

| Library | Role |
|---------|------|
| [Streamlit](https://streamlit.io) | Web app framework and reactive UI |
| [Plotly](https://plotly.com/python/) | Interactive charts and visualisations |
| [Pandas](https://pandas.pydata.org) | Data handling and filtering |

---

## 🖥️ Run it locally

**1. Clone the repository**
```bash
git clone https://github.com/your-username/global_gdp_app.git
cd global_gdp_app
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Launch the app**

The app will open at `http://localhost:8501`.

---

## 📊 The dataset

The dataset covers **57 economies** across 9 regions, sourced from IMF and World Bank 2023 estimates. Each country record includes:

- **Nominal GDP** — in billions USD, current prices
- **Real GDP** — in billions USD, constant 2015 prices
- **Population** — in millions
- **GDP per Capita** — in USD

Regions covered: North America, Central America, South America, Europe, Middle East, Africa, South Asia, East Asia, and Oceania.

---

## 👤 Author

**Feda Mohammadi**  
Quantitative Economics and Mathematics

📧 [mohammadif@berea.edu](mailto:mohammadif@berea.edu)
