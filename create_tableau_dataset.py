from pathlib import Path

import pandas as pd


# Project folders
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Input files
HISTORICAL_FILE = DATA_DIR / "historical_demand_clean.csv"
FES_FILE = DATA_DIR / "energy_demand_clean.csv"
AI_FILE = DATA_DIR / "ml_prediction.csv"

# Output file for Tableau
OUTPUT_FILE = DATA_DIR / "tableau_demand_data.csv"


# Check required files exist
required_files = [
    HISTORICAL_FILE,
    FES_FILE,
    AI_FILE,
]

for file_path in required_files:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file not found: {file_path}"
        )


# Load datasets
historical_df = pd.read_csv(HISTORICAL_FILE)
fes_df = pd.read_csv(FES_FILE)
ai_df = pd.read_csv(AI_FILE)


# Prepare historical data
historical_tableau = historical_df[
    ["Year", "Demand"]
].copy()

historical_tableau["Source"] = "Historical Data"
historical_tableau["Scenario"] = "Historical Demand"
historical_tableau["Series Type"] = "Historical"


# Prepare FES scenario data
fes_tableau = fes_df[
    ["Source", "Scenario", "Year", "Demand"]
].copy()

fes_tableau["Series Type"] = "FES Scenario"


# Prepare AI forecast data
ai_tableau = ai_df[
    ["Source", "Scenario", "Year", "Demand"]
].copy()

ai_tableau["Series Type"] = "AI Forecast"


# Combine all datasets
tableau_df = pd.concat(
    [
        historical_tableau,
        fes_tableau,
        ai_tableau,
    ],
    ignore_index=True,
)


# Convert columns to the correct types
tableau_df["Year"] = pd.to_numeric(
    tableau_df["Year"],
    errors="coerce",
)

tableau_df["Demand"] = pd.to_numeric(
    tableau_df["Demand"],
    errors="coerce",
)


# Remove invalid or incomplete rows
tableau_df = tableau_df.dropna(
    subset=[
        "Series Type",
        "Source",
        "Scenario",
        "Year",
        "Demand",
    ]
).copy()


tableau_df["Year"] = tableau_df["Year"].astype(int)

tableau_df["Source"] = (
    tableau_df["Source"]
    .astype(str)
    .str.strip()
)

tableau_df["Scenario"] = (
    tableau_df["Scenario"]
    .astype(str)
    .str.strip()
)


# Arrange columns for Tableau
tableau_df = tableau_df[
    [
        "Series Type",
        "Source",
        "Scenario",
        "Year",
        "Demand",
    ]
]


# Remove duplicates and sort
tableau_df = tableau_df.drop_duplicates()

tableau_df = tableau_df.sort_values(
    [
        "Series Type",
        "Source",
        "Scenario",
        "Year",
    ]
).reset_index(drop=True)


# Save the Tableau-ready CSV
tableau_df.to_csv(
    OUTPUT_FILE,
    index=False,
)


print("Tableau dataset created successfully.")
print(f"Saved to: {OUTPUT_FILE}")
print(f"Rows exported: {len(tableau_df):,}")
print()
print(tableau_df.head(10))