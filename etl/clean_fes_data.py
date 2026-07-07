import pandas as pd
from pathlib import Path


def clean_fes(file_path: Path, source_name: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()

    print(f"\nProcessing {file_path.name}")
    print("Columns:", df.columns.tolist())

    # Standardise Scenario/Pathway column name
    if "Scenario" in df.columns:
        scenario_col = "Scenario"
    elif "Pathway" in df.columns:
        scenario_col = "Pathway"
    else:
        raise ValueError(
            f"{file_path.name} is missing both 'Scenario' and 'Pathway'. "
            f"Available columns: {df.columns.tolist()}"
        )

    df = df.rename(columns={scenario_col: "Scenario"})

    # Show unique scenario/pathway values
    print("Available scenario values:")
    print(df["Scenario"].dropna().unique())

    # TEMP: do not filter yet
    df = df[df["Data item"] == "GBFES System Demand: Total"].copy()

    df = df.melt(
        id_vars=["Scenario"],
        var_name="Year",
        value_name="Demand"
    )

    df = df[df["Year"].astype(str).str.isnumeric()].copy()
    df["Year"] = df["Year"].astype(int)
    df["Demand"] = pd.to_numeric(df["Demand"], errors="coerce")

    df["Source"] = source_name
    df = df[["Source", "Scenario", "Year", "Demand"]]

    return df


def main():
    base_dir = Path(r"C:\Users\Jevha\OneDrive\Documents\Personal Project - AWE\Energy-Consumption-Analytics-Dashboard")
    raw_dir = base_dir / "data" / "raw" / "Electricity Demand Summary Data"
    output_file = base_dir / "data" / "processed" / "energy_demand_clean.csv"

    output_file.parent.mkdir(parents=True, exist_ok=True)

    files = [
        (raw_dir / "fes2023_ed1_v001.csv", "FES 2023"),
        (raw_dir / "fes2024_ed1_v002.csv", "FES 2024"),
        (raw_dir / "fes2025_ed1_v006.csv", "FES 2025"),
    ]

    cleaned = []
    for file_path, source_name in files:
        cleaned.append(clean_fes(file_path, source_name))

    final_df = pd.concat(cleaned, ignore_index=True)
    final_df = final_df.sort_values(by=["Source", "Scenario", "Year"]).reset_index(drop=True)

    final_df.to_csv(output_file, index=False)

    print(f"\nDone. Saved to:\n{output_file}")

if __name__ == "__main__":
    main()