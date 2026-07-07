import pandas as pd
from pathlib import Path

folder = Path("data/raw/Historical Demand Data")

results = []

for file in sorted(folder.glob("*.csv")):
    df = pd.read_csv(file, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["SETTLEMENT_DATE"], errors="coerce")
    df = df.dropna(subset=["Date"]).copy()
    df["Year"] = df["Date"].dt.year

    for col in ["ND", "TSD"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            energy_gwh = (df[col].fillna(0) * 0.5).sum() / 1000
            results.append({
                "File": file.name,
                "Year": int(df["Year"].iloc[0]),
                "Measure": col,
                "Demand_GWh": energy_gwh
            })

check_df = pd.DataFrame(results)
print(check_df.sort_values(["Year", "Measure"]))