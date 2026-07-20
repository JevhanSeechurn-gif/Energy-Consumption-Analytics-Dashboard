from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Forecast",
    page_icon="🤖",
    layout="wide",
)


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

PAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PAGE_DIR.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"

HISTORICAL_FILE = DATA_DIR / "historical_demand_clean.csv"
FES_FILE = DATA_DIR / "energy_demand_clean.csv"
ML_FILE = DATA_DIR / "ml_prediction.csv"


# ---------------------------------------------------------
# Data loading
# ---------------------------------------------------------

@st.cache_data
def load_data():
    historical_df = pd.read_csv(HISTORICAL_FILE)
    fes_df = pd.read_csv(FES_FILE)
    ml_df = pd.read_csv(ML_FILE)

    # Convert important columns to numeric
    historical_df["Year"] = pd.to_numeric(
        historical_df["Year"],
        errors="coerce",
    )
    historical_df["Demand"] = pd.to_numeric(
        historical_df["Demand"],
        errors="coerce",
    )

    fes_df["Year"] = pd.to_numeric(
        fes_df["Year"],
        errors="coerce",
    )
    fes_df["Demand"] = pd.to_numeric(
        fes_df["Demand"],
        errors="coerce",
    )

    ml_df["Year"] = pd.to_numeric(
        ml_df["Year"],
        errors="coerce",
    )
    ml_df["Demand"] = pd.to_numeric(
        ml_df["Demand"],
        errors="coerce",
    )

    # Remove invalid or blank rows
    historical_df = historical_df.dropna(
        subset=["Year", "Demand"]
    )

    fes_df = fes_df.dropna(
        subset=["Source", "Scenario", "Year", "Demand"]
    )

    ml_df = ml_df.dropna(
        subset=["Year", "Demand"]
    )

    # Ensure years are integers
    historical_df["Year"] = historical_df["Year"].astype(int)
    fes_df["Year"] = fes_df["Year"].astype(int)
    ml_df["Year"] = ml_df["Year"].astype(int)

    # Sort chronologically
    historical_df = historical_df.sort_values("Year")
    fes_df = fes_df.sort_values(
        ["Source", "Scenario", "Year"]
    )
    ml_df = ml_df.sort_values("Year")

    return historical_df, fes_df, ml_df


try:
    historical_df, fes_df, ml_df = load_data()
except FileNotFoundError as error:
    st.error(f"Required data file was not found:\n\n{error}")
    st.stop()
except Exception as error:
    st.error(f"An error occurred while loading the data:\n\n{error}")
    st.stop()


# ---------------------------------------------------------
# Page heading
# ---------------------------------------------------------

st.title("🤖 AI Electricity Demand Forecast")

st.write(
    """
    This page compares historical GB electricity demand, a Linear Regression
    forecast trained on historical observations, and official NESO Future
    Energy Scenarios.
    """
)


# ---------------------------------------------------------
# Filters
# ---------------------------------------------------------

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    available_editions = sorted(
        fes_df["Source"].dropna().unique()
    )

    selected_edition = st.selectbox(
        "Select FES edition",
        options=available_editions,
        index=len(available_editions) - 1,
    )

edition_df = fes_df[
    fes_df["Source"] == selected_edition
].copy()

with filter_col2:
    available_scenarios = sorted(
        edition_df["Scenario"].dropna().unique()
    )

    selected_scenarios = st.multiselect(
        "Select official scenarios",
        options=available_scenarios,
        default=available_scenarios,
    )


# ---------------------------------------------------------
# Apply filters
# ---------------------------------------------------------

if selected_scenarios:
    filtered_fes_df = edition_df[
        edition_df["Scenario"].isin(selected_scenarios)
    ].copy()
else:
    filtered_fes_df = edition_df.iloc[0:0].copy()


# ---------------------------------------------------------
# KPI calculations
# ---------------------------------------------------------

latest_historical_row = historical_df.loc[
    historical_df["Year"].idxmax()
]

latest_historical_year = int(latest_historical_row["Year"])
latest_historical_demand = latest_historical_row["Demand"]

ml_2050_rows = ml_df[ml_df["Year"] == 2050]

if not ml_2050_rows.empty:
    ml_2050_demand = ml_2050_rows.iloc[0]["Demand"]
else:
    ml_2050_demand = None

fes_2050_df = filtered_fes_df[
    filtered_fes_df["Year"] == 2050
]

if not fes_2050_df.empty:
    highest_fes_2050 = fes_2050_df.loc[
        fes_2050_df["Demand"].idxmax()
    ]

    lowest_fes_2050 = fes_2050_df.loc[
        fes_2050_df["Demand"].idxmin()
    ]
else:
    highest_fes_2050 = None
    lowest_fes_2050 = None


# ---------------------------------------------------------
# KPI display
# ---------------------------------------------------------

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label=f"Historical demand ({latest_historical_year})",
        value=f"{latest_historical_demand:,.0f} GWh",
    )

with kpi2:
    if ml_2050_demand is not None:
        st.metric(
            label="AI forecast for 2050",
            value=f"{ml_2050_demand:,.0f} GWh",
        )
    else:
        st.metric(
            label="AI forecast for 2050",
            value="Not available",
        )

with kpi3:
    if highest_fes_2050 is not None:
        st.metric(
            label="Highest selected FES 2050",
            value=f"{highest_fes_2050['Demand']:,.0f} GWh",
            help=str(highest_fes_2050["Scenario"]),
        )
        st.caption(highest_fes_2050["Scenario"])
    else:
        st.metric(
            label="Highest selected FES 2050",
            value="Not available",
        )

with kpi4:
    if lowest_fes_2050 is not None:
        st.metric(
            label="Lowest selected FES 2050",
            value=f"{lowest_fes_2050['Demand']:,.0f} GWh",
            help=str(lowest_fes_2050["Scenario"]),
        )
        st.caption(lowest_fes_2050["Scenario"])
    else:
        st.metric(
            label="Lowest selected FES 2050",
            value="Not available",
        )


# ---------------------------------------------------------
# Main comparison chart
# ---------------------------------------------------------

st.subheader("Historical, AI and official scenario comparison")

figure = go.Figure()

# Historical line
figure.add_trace(
    go.Scatter(
        x=historical_df["Year"],
        y=historical_df["Demand"],
        mode="lines+markers",
        name="Historical demand",
        line=dict(width=4),
    )
)

# AI forecast line
figure.add_trace(
    go.Scatter(
        x=ml_df["Year"],
        y=ml_df["Demand"],
        mode="lines+markers",
        name="AI forecast – Linear Regression",
        line=dict(width=4, dash="dash"),
    )
)

# Official FES scenario lines
for scenario in selected_scenarios:
    scenario_df = filtered_fes_df[
        filtered_fes_df["Scenario"] == scenario
    ].sort_values("Year")

    if scenario_df.empty:
        continue

    figure.add_trace(
        go.Scatter(
            x=scenario_df["Year"],
            y=scenario_df["Demand"],
            mode="lines",
            name=f"{selected_edition} – {scenario}",
            line=dict(width=2),
        )
    )

figure.update_layout(
    title=(
        "GB electricity demand: historical data, "
        "AI forecast and NESO scenarios"
    ),
    xaxis_title="Year",
    yaxis_title="Electricity demand (GWh)",
    hovermode="x unified",
    legend_title="Data series",
    height=650,
)

figure.update_xaxes(
    dtick=5,
    showgrid=True,
)

figure.update_yaxes(
    tickformat=",",
    showgrid=True,
)

st.plotly_chart(
    figure,
    use_container_width=True,
)


# ---------------------------------------------------------
# Explanation
# ---------------------------------------------------------

st.subheader("How to interpret the comparison")

st.info(
    """
    The Linear Regression model extrapolates the pattern found in historical
    demand data. It uses year as its only input and therefore does not account
    for future policy, economic conditions, electrification, electric vehicle
    adoption, heat pumps, industrial change or data-centre growth.

    NESO scenarios use broader assumptions about how the energy system may
    change. Therefore, the AI forecast is not expected to match the official
    scenarios.
    """
)


# ---------------------------------------------------------
# Dynamic observations
# ---------------------------------------------------------

st.subheader("Key observations")

historical_start = historical_df.iloc[0]
historical_end = historical_df.iloc[-1]

historical_change = (
    (
        historical_end["Demand"]
        - historical_start["Demand"]
    )
    / historical_start["Demand"]
) * 100

st.write(
    f"""
    - Historical demand changed by **{historical_change:.1f}%**
      between **{int(historical_start['Year'])}** and
      **{int(historical_end['Year'])}**.
    """
)

if ml_2050_demand is not None:
    ml_change = (
        (
            ml_2050_demand
            - latest_historical_demand
        )
        / latest_historical_demand
    ) * 100

    direction = "increase" if ml_change >= 0 else "decrease"

    st.write(
        f"""
        - The Linear Regression model projects a
          **{abs(ml_change):.1f}% {direction}** between
          {latest_historical_year} and 2050.
        """
    )

if highest_fes_2050 is not None and ml_2050_demand is not None:
    difference = (
        highest_fes_2050["Demand"]
        - ml_2050_demand
    )

    st.write(
        f"""
        - The highest selected official scenario in 2050 is
          **{highest_fes_2050['Scenario']}**, which is
          **{difference:,.0f} GWh higher** than the AI forecast.
        """
    )


# ---------------------------------------------------------
# Data tables
# ---------------------------------------------------------

with st.expander("View AI forecast data"):
    st.dataframe(
        ml_df,
        use_container_width=True,
        hide_index=True,
    )

with st.expander("View selected official scenario data"):
    st.dataframe(
        filtered_fes_df,
        use_container_width=True,
        hide_index=True,
    )

with st.expander("View historical data"):
    st.dataframe(
        historical_df,
        use_container_width=True,
        hide_index=True,
    )