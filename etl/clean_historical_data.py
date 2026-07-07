import pandas as pd
from pathlib import Path


def clean_historical(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()

    print(f"\nProcessing {file_path.name}")
    print("Columns:", df.columns.tolist())

    required_columns = ["SETTLEMENT_DATE", "ND"]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(
            f"{file_path.name} is missing required columns: {missing}\n"
            f"Available columns: {df.columns.tolist()}"
        )

    # Handle mixed date formats across years
    df["Date"] = pd.to_datetime(df["SETTLEMENT_DATE"], errors="coerce")
    df = df.dropna(subset=["Date"]).copy()

    # Ensure demand is numeric
    df["ND"] = pd.to_numeric(df["ND"], errors="coerce")
    df = df.dropna(subset=["ND"]).copy()

    # Extract year
    df["Year"] = df["Date"].dt.year

    # Convert MW for half-hour period into MWh
    df["Energy_MWh"] = df["ND"] * 0.5

    # Aggregate yearly and convert to GWh
    df_year = (
        df.groupby("Year", as_index=False)["Energy_MWh"]
        .sum()
        .rename(columns={"Energy_MWh": "Demand"})
    )
    df_year["Demand"] = df_year["Demand"] / 1000

    # Add source label
    df_year["Source"] = "Historical"

    # Final column order
    df_year = df_year[["Source", "Year", "Demand"]]

    return df_year


def main():
    base_dir = Path(r"C:\Users\Jevha\OneDrive\Documents\Personal Project - AWE\Energy-Consumption-Analytics-Dashboard")
    raw_dir = base_dir / "data" / "raw" / "Historical Demand Data"
    output_file = base_dir / "data" / "processed" / "historical_demand_clean.csv"

    output_file.parent.mkdir(parents=True, exist_ok=True)

    files = sorted(raw_dir.glob("*.csv"))

    if not files:
        raise FileNotFoundError(f"No CSV files found in: {raw_dir}")

    cleaned = []
    for file_path in files:
        cleaned.append(clean_historical(file_path))

    final_df = pd.concat(cleaned, ignore_index=True)

    # Remove duplicates in case one file somehow contains overlapping yearly totals
    final_df = final_df.drop_duplicates(subset=["Year"]).sort_values(by="Year").reset_index(drop=True)

    final_df.to_csv(output_file, index=False)

    print(f"\nDone. Saved to:\n{output_file}")
    print("\nPreview:")
    print(final_df)


if __name__ == "__main__":
    main()