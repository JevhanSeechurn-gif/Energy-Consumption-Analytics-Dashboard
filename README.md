# UK Electricity Demand Analytics Dashboard
---

## Tools Used

| Tool | Version | Purpose |
|---|---|---|
|[Python](https://www.python.org/) | 3.10+ | Core language |
| [CSV](https://docs.python.org/3/library/csv.html) | N/A | Data source — stores all energy data for the dashboard (no database setup required) |
| [Pandas](https://pandas.pydata.org/) | latest | ETL pipeline — cleans and loads data |
| [Streamlit](https://streamlit.io/) | latest | Dashboard front end |
| [Plotly](https://plotly.com/) | latest | Charts and visualisations |
| [Claude API](https://www.anthropic.com/) | latest | AI chatbot — natural language to SQL |
| [psycopg2](https://pypi.org/project/psycopg2/) | latest | Connects Python to PostgreSQL |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | latest | Manages API keys and credentials |
| [Power BI](https://powerbi.microsoft.com/) | Latest | Creates business reporting dashboards (non-AI) |
| [Tableau](https://www.tableau.com/) | Latest | Creates interactive visualizations and data storytelling dashboards |

---

## Live Demo

🔗 [View Dashboard](#)

![Dashboard Screenshot](assets/dashboard-screenshot.png)

---

## Project Overview

This is a analytical dashboard that explores historical electrcity demands throughout Great Britain from 2015 to 2025, as well comparing future scenarios with National Grid ESO. The project consists of data processing, interactive visualisations, KPI analysis and machine-learning demand forecast, with resutls displayed via streamlit, tableau and Power BI.

---

## Features

- Interactive dashboard exploring historical Great Britain electricity demand from 2015 to 2025
- Comparison of National Grid ESO Future Energy Scenarios across multiple forecast years
- Long-term demand projections extending to 2050
- KPI analysis showing the latest demand, historical highs and lows, and future scenario comparisons
- Machine-learning demand forecast displayed alongside official National Grid ESO projections
- Interactive filtering by scenario, pathway, source and year
- Clear visualisations created in Streamlit, Tableau and Power BI
- Data processing pipeline built with Python and Pandas

---

## Data Sources

| Dataset | Source | Coverage |
|---|---|---|
| Historical Electricity Demand | National Grid ESO / NESO | 2015–2025 |
| Future Energy Scenarios 2023 | National Grid ESO | Forecasts to 2050 |
| Future Energy Scenarios 2024 | National Grid ESO | Forecasts to 2050 |
| Future Energy Scenarios 2025 | National Grid ESO / NESO | Forecasts to 2050 |
| Machine-Learning Forecast | Generated within this project | Short-term demand forecast |

---

## Database Schema

```The dataset is structured in a tabular format, with each row representing energy consumption by source and year. Key fields include:

Year
Energy Source (e.g. fossil fuels, nuclear, renewables)
Consumption Value (e.g. TWh or %)

This structure enables straightforward time-series analysis and comparison across energy types.

```

---

## Project Structure

```
project-name/
│
├── data/
│   └── raw/
│
├── etl/
│   ├── clean.py
│   └── load.py
│
├── sql/
│   └── queries.sql
│
├── dashboard/
│   ├── app.py
│   ├── charts.py
│   └── chatbot.py
│
├── assets/
├── DESIGN.md
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.10+ – Core language for ETL, dashboard, and AI integration.
- PostgreSQL 14+ – Database to store energy consumption data.
- pip (Python package manager) – To install required Python libraries.


---

### Installation

```bash

```

### Environment Variables

```

```

### Running the ETL Pipeline

```bash

```

### Running the Dashboard

```bash

```

---

## SQL Queries

-
-
-

---

## Key Findings

-
-
-

---

## AI Chatbot

---

## Roadmap

- [ ]
- [ ]
- [ ]
- [ ]
- [ ]

---

## Author

**Name** — Degree, University, Year

[LinkedIn](#) | [Portfolio](#) | [GitHub](#)

---

## Licence
