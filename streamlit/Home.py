import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="UK Electricity Demand Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- DATA PATHS ----------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data" / "processed"

historical_df = pd.read_csv(DATA_DIR / "historical_demand_clean.csv")
fes_df = pd.read_csv(DATA_DIR / "energy_demand_clean.csv")

# ---------- KPI CALCULATIONS ----------
latest_year = historical_df["Year"].max()
latest_demand = historical_df.loc[
    historical_df["Year"] == latest_year, "Demand"
].iloc[0]

previous_year = latest_year - 1
previous_demand = historical_df.loc[
    historical_df["Year"] == previous_year, "Demand"
].iloc[0]

latest_change = ((latest_demand - previous_demand) / previous_demand) * 100

fes_2050 = fes_df[fes_df["Year"] == 2050]
highest_2050 = fes_2050["Demand"].max()
lowest_2050 = fes_2050["Demand"].min()

min_year = min(historical_df["Year"].min(), fes_df["Year"].min())
max_year = max(historical_df["Year"].max(), fes_df["Year"].max())

highest_scenario = fes_2050.loc[
    fes_2050["Demand"].idxmax(), "Scenario"
]

lowest_scenario = fes_2050.loc[
    fes_2050["Demand"].idxmin(), "Scenario"
]

# ---------- STYLING ----------
st.markdown("""
<style>
@keyframes fadeInPage {
    from { opacity: 0; }
    to { opacity: 1; }
}

.main {
    animation: fadeInPage 1.2s ease-in;
}

div[data-testid="stMetric"] {
    animation: fadeInPage 1.2s ease-in;
    background-color: white;
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

div[data-testid="stMetric"] div {
    color: black !important;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
    padding: 10px;
    font-size: 14px;
    z-index: 9999;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.header("UK Electricity Demand Dashboard", divider="rainbow")
st.caption("Historical analysis, FES scenarios, and predictive modelling")

# ---------- KPI CARDS ----------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Latest Historical Demand",
        f"{latest_demand:,.0f} GWh",
        f"{latest_change:+.1f}% vs {previous_year}"
    )

with col2:
    st.metric(
        "Highest Future Demand 2050",
        f"{highest_2050:,.0f} GWh",
        highest_scenario
    )

with col3:
    st.metric(
        "Lowest Future Demand 2050",
        f"{lowest_2050:,.0f} GWh",
        lowest_scenario
    )

with col4:
    st.metric(
        "Data Coverage",
        f"{min_year} – {max_year}",
        "Historic + Forecast"
    )

st.divider()

# ---------- OVERVIEW ----------
left, right = st.columns([1, 2])

with left:
    st.subheader("Project Overview")
    st.write(
        "This dashboard explores UK electricity demand using historical data, "
        "official NESO Future Energy Scenario forecasts, and predictive modelling."
    )

with right:
    st.subheader("Key Focus")
    st.write(
        "Compare past electricity demand, future scenario-based forecasts, "
        "and a model-generated prediction to understand how UK demand may change by 2050."
    )

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
    <p>Developed by Jevhan Seechurn 2026</p>
</div>
""", unsafe_allow_html=True)