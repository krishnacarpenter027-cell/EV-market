# Electric Vehicle Market Performance & Insights

A runnable interactive dashboard for the EV market project shown in your screenshots.

## What is included
- `app.py` — interactive dashboard with filters and charts
- `data/ev_market_sample.csv` — sample dataset for the dashboard
- `data/ev_market_sample.xlsx` — same dataset in Excel format
- `tableau/` — Tableau build guide and calculated-field suggestions
- `report/` — project report draft
- `presentation/` — presentation outline
- `requirements.txt` — Python packages

## Run the working dashboard (Windows)
1. Install Python 3.10 or newer from https://www.python.org/downloads/
2. Extract this ZIP folder.
3. Open the extracted folder in VS Code.
4. Open Terminal > New Terminal.
5. Run:
   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```
6. The dashboard will open in your browser. If it does not, open the local URL printed in the terminal (usually http://localhost:8501).

## Important data note
The included dataset is synthetic sample data created for demonstrating the workflow and dashboard. It is NOT verified real-world EV market data. Clearly label it as sample data in any submission, or replace it with your teacher-approved / sourced dataset before presenting factual conclusions.

## Tableau
Import `data/ev_market_sample.xlsx` into Tableau Desktop/Public. Follow `tableau/TABLEAU_GUIDE.md` to create the equivalent workbook and dashboards.
