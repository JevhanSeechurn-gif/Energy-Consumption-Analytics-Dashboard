from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


# ---------------------------------------------------------
# 1. File paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"

HISTORICAL_FILE = DATA_DIR / "historical_demand_clean.csv"
OUTPUT_FILE = DATA_DIR / "ml_prediction.csv"


# ---------------------------------------------------------
# 2. Load and prepare the historical data
# ---------------------------------------------------------

historical_df = pd.read_csv(HISTORICAL_FILE)

# Keep only the columns required by the model
historical_df = historical_df[["Year", "Demand"]].copy()

# Convert values to numeric and remove invalid rows
historical_df["Year"] = pd.to_numeric(
    historical_df["Year"],
    errors="coerce",
)

historical_df["Demand"] = pd.to_numeric(
    historical_df["Demand"],
    errors="coerce",
)

historical_df = historical_df.dropna()
historical_df = historical_df.sort_values("Year")


# ---------------------------------------------------------
# 3. Create chronological training and testing data
# ---------------------------------------------------------

# Train using 2015–2022
train_df = historical_df[historical_df["Year"] <= 2022]

# Test using 2023–2025
test_df = historical_df[historical_df["Year"] > 2022]

X_train = train_df[["Year"]]
y_train = train_df["Demand"]

X_test = test_df[["Year"]]
y_test = test_df["Demand"]


# ---------------------------------------------------------
# 4. Train the regression model
# ---------------------------------------------------------

model = LinearRegression()
model.fit(X_train, y_train)


# ---------------------------------------------------------
# 5. Test the model
# ---------------------------------------------------------

test_predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, test_predictions)
mse = mean_squared_error(y_test, test_predictions)
rmse = mse ** 0.5
r2 = r2_score(y_test, test_predictions)

test_results = test_df.copy()
test_results["Predicted Demand"] = test_predictions
test_results["Error"] = (
    test_results["Demand"] - test_results["Predicted Demand"]
)

print("\nMODEL TEST RESULTS")
print("-" * 50)
print(test_results.to_string(index=False))

print("\nMODEL PERFORMANCE")
print("-" * 50)
print(f"Mean Absolute Error: {mae:,.2f} GWh")
print(f"Root Mean Squared Error: {rmse:,.2f} GWh")
print(f"R² Score: {r2:.4f}")

print("\nMODEL COEFFICIENTS")
print("-" * 50)
print(f"Annual change: {model.coef_[0]:,.2f} GWh per year")
print(f"Intercept: {model.intercept_:,.2f}")


# ---------------------------------------------------------
# 6. Retrain using all historical data
# ---------------------------------------------------------

X_all = historical_df[["Year"]]
y_all = historical_df["Demand"]

final_model = LinearRegression()
final_model.fit(X_all, y_all)


# ---------------------------------------------------------
# 7. Forecast demand from 2026 to 2050
# ---------------------------------------------------------

future_years = pd.DataFrame(
    {"Year": range(2026, 2051)}
)

future_predictions = final_model.predict(future_years)

forecast_df = pd.DataFrame(
    {
        "Source": "AI Forecast",
        "Scenario": "Linear Regression",
        "Year": future_years["Year"],
        "Demand": future_predictions,
    }
)

forecast_df.to_csv(OUTPUT_FILE, index=False)

print("\nFORECAST")
print("-" * 50)
print(forecast_df.to_string(index=False))

print(f"\nForecast saved to:\n{OUTPUT_FILE}")


# ---------------------------------------------------------
# 8. Display the historical and forecast graph
# ---------------------------------------------------------

plt.figure(figsize=(11, 6))

plt.plot(
    historical_df["Year"],
    historical_df["Demand"],
    marker="o",
    label="Historical Demand",
)

plt.plot(
    forecast_df["Year"],
    forecast_df["Demand"],
    marker="o",
    label="Linear Regression Forecast",
)

plt.xlabel("Year")
plt.ylabel("Electricity Demand (GWh)")
plt.title("Historical Electricity Demand and Regression Forecast")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()