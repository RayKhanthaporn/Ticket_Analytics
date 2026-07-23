# Ticket Analytics

This project combines a Jupyter notebook workflow and a Streamlit-based ticket analytics assistant using AI agent for exploring and summarising ticket data.

## Project overview

The repository contains:

- [Ticket_Analytics.ipynb](Ticket_Analytics.ipynb) — notebook for data exploration, enrichment, and analysis
- [streamlit_ticket_agent.py](streamlit_ticket_agent.py) — Streamlit app is AI Agent for interactive ticket insights and question answering
- [requirements.txt](requirements.txt) — Python dependencies for the notebook and app

## Project lineage

The project evolved in stages:

1. Data preparation and enrichment in the notebook
   - loading ticket data
   - joining holiday and regional context
   - creating derived fields for analysis
2. Exploratory analytics and insight generation
   - reviewing ticket volume, categories, teams, and holiday impact
3. Streamlit application deployment
   - turning the analysis into a simple interactive app for operational users

This lineage keeps the notebook as the analytical foundation and the Streamlit app as the presentation layer.

## Files in this repository

- [Ticket_Analytics.ipynb](Ticket_Analytics.ipynb)
  - Jupyter notebook for data prep and analysis
- [streamlit_ticket_agent.py](streamlit_ticket_agent.py)
  - Streamlit dashboard and Q&A experience
- [requirements.txt](requirements.txt)
  - Required Python packages
- [TechSolve - Ticket Data.xlsx](TechSolve%20-%20Ticket%20Data.xlsx)
  - Source ticket workbook used in the analysis workflow

## Requirements

- Python 3.10 or newer
- pip
- Optional: Jupyter support in VS Code

## Setup

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If you want to run the notebook in VS Code, also install:

```bash
pip install jupyter ipykernel
```

## Run the Streamlit app

From the project root:

```bash
streamlit run streamlit_ticket_agent.py
```

Or:

```bash
python -m streamlit run streamlit_ticket_agent.py
```

Open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Environment variables

The app can run with the default dataset path, but you can override it if needed.

### Optional variables

- `OPENAI_API_KEY`
  - Used when the app calls OpenAI for answer generation
- `TICKET_DATA_PATH`
  - Overrides the default data file location

Example for Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key"
$env:TICKET_DATA_PATH="path\to\your\data.csv"
```

Example for macOS / Linux:

```bash
export OPENAI_API_KEY="your_api_key"
export TICKET_DATA_PATH="path/to/your/data.csv"
```

## Run the notebook

Open [Ticket_Analytics.ipynb](Ticket_Analytics.ipynb) in VS Code or Jupyter Notebook and run the cells in order.

## Notes

- The Streamlit app expects the processed ticket data to be available in the project environment.
- If the default dataset path is missing, the app will show an error and prompt you to set `TICKET_DATA_PATH`.
- For AI-assisted answers, an OpenAI API key is required.
