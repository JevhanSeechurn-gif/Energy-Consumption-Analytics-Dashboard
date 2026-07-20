import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.markdown("""
<style>
@keyframes fadeInPage {
    from {opacity:0;}
    to {opacity:1;}
}

.main{
    animation:fadeInPage 1.2s ease-in;
}

div[data-testid="stMetric"]{
    background-color:white;
    border-radius:8px;
    padding:16px;
    box-shadow:0 2px 8px rgba(0,0,0,0.08);
}

div[data-testid="stMetric"] div{
    color:black !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Historical Trends",
    layout="wide"
)

st.title("📈 Historical Trends")

st.write(
    "Explore how UK electricity demand has changed between 2015 and 2025 using historical data."
)

# -------------------------------
# LOAD DATA
# -------------------------------

DATA_DIR = Path(
    r"C:\Users\Jevha\OneDrive\Documents\Personal Project - AWE\Energy-Consumption-Analytics-Dashboard\data\processed"
)

df = pd.read_csv(DATA_DIR / "historical_demand_clean.csv")

# -------------------------------
# KPI CALCULATIONS
# -------------------------------
latest = df.iloc[-1]["Demand"]
highest = df["Demand"].max()
lowest = df["Demand"].min()
average = df["Demand"].mean()

highest_year = df.loc[df["Demand"].idxmax(), "Year"]
lowest_year = df.loc[df["Demand"].idxmin(), "Year"]

overall_change = (
    (df.iloc[-1]["Demand"] - df.iloc[0]["Demand"])
    / df.iloc[0]["Demand"]
) * 100

latest_year = df["Year"].max()
start_year = df["Year"].min()
end_year = df["Year"].max()
# -------------------------------
# KPI CARDS
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Latest Demand",
        f"{latest:,.0f} GWh",
        f"{latest_year}"
    )

with col2:
    st.metric(
        "Highest Demand",
        f"{highest:,.0f} GWh",
        f"{highest_year}"
    )

with col3:
    st.metric(
        "Lowest Demand",
        f"{lowest:,.0f} GWh",
        f"{lowest_year}"
    )

with col4:
    st.metric(
        "Average Demand",
        f"{average:,.0f} GWh",
        f"{start_year}–{end_year}"
    )

st.divider()

# -------------------------------
# LINE CHART
# -------------------------------
fig = px.line(
    df,
    x="Year",
    y="Demand",
    markers=True,
    title="UK Historical Electricity Demand (2015–2025)"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Electricity Demand (GWh)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------
# KEY INSIGHTS
# -------------------------------
st.subheader("📊 Key Insights")

st.markdown(f"""
- Electricity demand changed by **{overall_change:.1f}%** between **{df.iloc[0]['Year']}** and **{df.iloc[-1]['Year']}**.
- The **highest recorded demand** occurred in **{highest_year}** at **{highest:,.0f} GWh**.
- The **lowest recorded demand** occurred in **{lowest_year}** at **{lowest:,.0f} GWh**.
- Electricity demand generally declined over the period before stabilising in the final years of the dataset.
""")