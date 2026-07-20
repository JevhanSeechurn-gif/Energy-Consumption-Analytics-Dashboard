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

- Interactive dashboard to explore UK energy consumption trends (2018–2023)
- Comparison of energy sources, including fossil fuels, nuclear, and renewables
- Time-based analysis to track changes in energy mix over the selected period
- Clear visualisations designed for quick insight and easy interpretation

---

## Data Sources

| Dataset | Source | Coverage |
|-----|-----|-----|
|UK Energy Consumption Data|UK Government / ONS / BEIS |2018–2023 |
|Renewable Energy Statistics |Official UK energy datasets |2018–2023 |

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
