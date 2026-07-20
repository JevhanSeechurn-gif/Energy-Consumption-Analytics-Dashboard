import pandas as pd
from pathlib import Path


def clean_fes(file_path: Path, source_name: str) -> pd.DataFrame:
    """
    Clean one NESO FES electricity-demand CSV.

    Output columns:
        Source, Scenario, Year, Demand
    """

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(
        file_path,
        encoding="utf-8-sig",
        low_memory=False,
    )

    # Remove accidental spaces from column names
    df.columns = df.columns.astype(str).str.strip()

    print(f"\nProcessing: {file_path.name}")
    print(f"Rows before cleaning: {len(df):,}")

    # Some FES editions use Scenario; others use Pathway
    if "Scenario" in df.columns:
        scenario_col = "Scenario"
    elif "Pathway" in df.columns:
        scenario_col = "Pathway"
    else:
        raise ValueError(
            f"{file_path.name} has neither 'Scenario' nor 'Pathway'.\n"
            f"Available columns: {df.columns.tolist()}"
        )

    df = df.rename(columns={scenario_col: "Scenario"})

    # Required columns for filtering
    required_columns = {
        "Data item",
        "Scenario",
        "Fuel",
        "Peak/ Annual/ Minimum",
    }

    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        raise ValueError(
            f"{file_path.name} is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    # Clean text columns before filtering
    text_columns = [
        "Data item",
        "Scenario",
        "Fuel",
        "Peak/ Annual/ Minimum",
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    print("Available scenarios/pathways:")
    print(df["Scenario"].dropna().unique())

    # Keep only total annual electricity demand
    filtered_df = df[
        (df["Data item"] == "GBFES System Demand: Total")
        & (df["Fuel"] == "Electricity")
        & (
            df["Peak/ Annual/ Minimum"]
            .str.contains("Annual", case=False, na=False)
        )
    ].copy()

    if filtered_df.empty:
        raise ValueError(
            f"No total annual electricity-demand rows were found in "
            f"{file_path.name}."
        )

    print(f"Matching source rows: {len(filtered_df):,}")

    # Find columns whose names are four-digit years
    year_columns = [
        column
        for column in filtered_df.columns
        if str(column).strip().isdigit()
        and len(str(column).strip()) == 4
    ]

    if not year_columns:
        raise ValueError(
            f"No year columns were found in {file_path.name}."
        )

    # Convert wide format into long format
    cleaned_df = filtered_df.melt(
        id_vars=["Scenario"],
        value_vars=year_columns,
        var_name="Year",
        value_name="Demand",
    )

    # Convert values to the correct data types
    cleaned_df["Year"] = pd.to_numeric(
        cleaned_df["Year"],
        errors="coerce",
    )

    cleaned_df["Demand"] = pd.to_numeric(
        cleaned_df["Demand"],
        errors="coerce",
    )

    # Remove invalid years and unpublished blank forecasts
    cleaned_df = cleaned_df.dropna(
        subset=["Scenario", "Year", "Demand"]
    )

    cleaned_df["Year"] = cleaned_df["Year"].astype(int)

    # Add source edition
    cleaned_df["Source"] = source_name

    # Keep final dashboard-ready columns
    cleaned_df = cleaned_df[
        ["Source", "Scenario", "Year", "Demand"]
    ]

    # Remove accidental duplicate rows
    cleaned_df = cleaned_df.drop_duplicates(
        subset=["Source", "Scenario", "Year"],
        keep="first",
    )

    cleaned_df = cleaned_df.sort_values(
        by=["Scenario", "Year"]
    ).reset_index(drop=True)

    print(f"Rows after cleaning: {len(cleaned_df):,}")

    return cleaned_df


def main():
    base_dir = Path(
        r"C:\Users\Jevha\OneDrive\Documents"
        r"\Personal Project - AWE"
        r"\Energy-Consumption-Analytics-Dashboard"
    )

    raw_dir = (
        base_dir
        / "data"
        / "raw"
        / "Electricity Demand Summary Data"
    )

    output_file = (
        base_dir
        / "data"
        / "processed"
        / "energy_demand_clean.csv"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    files = [
        (
            raw_dir / "fes2023_ed1_v001.csv",
            "FES 2023",
        ),
        (
            raw_dir / "fes2024_ed1_v002.csv",
            "FES 2024",
        ),
        (
            raw_dir / "fes2025_ed1_v006.csv",
            "FES 2025",
        ),
    ]

    cleaned_frames = []

    for file_path, source_name in files:
        cleaned_df = clean_fes(
            file_path=file_path,
            source_name=source_name,
        )

        cleaned_frames.append(cleaned_df)

    final_df = pd.concat(
        cleaned_frames,
        ignore_index=True,
    )

    final_df = final_df.drop_duplicates(
        subset=["Source", "Scenario", "Year"],
        keep="first",
    )

    final_df = final_df.sort_values(
        by=["Source", "Scenario", "Year"]
    ).reset_index(drop=True)

    final_df.to_csv(
        output_file,
        index=False,
    )

    print("\nETL complete.")
    print(f"Total output rows: {len(final_df):,}")
    print(f"Saved to:\n{output_file}")

    print("\nRows by FES edition:")
    print(final_df.groupby("Source").size())

    print("\nAvailable scenarios/pathways:")
    print(
        final_df[
            ["Source", "Scenario"]
        ]
        .drop_duplicates()
        .sort_values(["Source", "Scenario"])
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()