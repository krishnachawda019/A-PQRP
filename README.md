# 📈 A-PQRP — AI-Powered Quant Research Platform

A full-stack platform for exploring, profiling, backtesting, and generating AI-assisted insights on stock market data. A-PQRP pairs a **FastAPI** backend for data processing and market access with a **Streamlit** dashboard for interactive analysis.

> Analyze · Backtest · Predict · Generate AI Insights

---

## ✨ Overview

A-PQRP is designed as a modular research workbench for quantitative finance. Users can upload their own datasets (CSV/Excel), pull live market data via Yahoo Finance, generate automated data profiling reports, and — as the platform matures — run backtests, train prediction models, and generate AI-written research summaries.

The project is in **active early development**. The architecture and API contracts are in place; several modules are scaffolded but not yet implemented (see [Project Status](#-project-status) below).

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI, Pydantic, Uvicorn |
| Frontend | Streamlit |
| Data Processing | pandas, numpy, openpyxl |
| Market Data | yfinance |
| Statistics / ML (planned) | statsmodels, scipy |
| Visualization | Plotly, Matplotlib, pydeck |

---

## 📂 Project Structure

```
A-PQRP/
├── backend/
│   ├── main.py                  # FastAPI app entrypoint & router registration
│   ├── config/
│   │   └── settings.py          # App configuration (scaffolded)
│   ├── routers/
│   │   ├── market.py            # GET /market/{symbol} — live quote data
│   │   ├── upload.py            # POST /upload — dataset ingestion
│   │   ├── profile.py           # GET /profile — dataset profiling report
│   │   ├── backtest.py          # (planned) strategy backtesting endpoints
│   │   ├── prediction.py        # (planned) ML prediction endpoints
│   │   ├── analytics.py         # (planned) analytics endpoints
│   │   └── report.py            # (planned) AI-generated report endpoints
│   ├── services/
│   │   ├── market_service.py    # yfinance integration
│   │   ├── upload_service.py    # file ingestion & in-memory dataframe store
│   │   ├── profile_service.py   # summary stats, missing values, dtypes, etc.
│   │   ├── indicator_service.py # (planned) technical indicators
│   │   ├── backtest_service.py  # (planned) backtesting engine
│   │   ├── prediction_service.py# (planned) forecasting models
│   │   └── report_service.py    # (planned) AI report generation
│   └── schemas/
│       ├── market_schema.py     # Pydantic response models for market data
│       └── upload_schema.py     # Pydantic response models for uploads
├── frontend/
│   ├── app.py                   # Streamlit entrypoint
│   ├── components/
│   │   ├── header.py            # Page header / branding
│   │   ├── sidebar.py           # Module navigation
│   │   ├── dashboard.py         # (planned) main dashboard view
│   │   ├── charts.py            # (planned) chart components
│   │   ├── metrics.py           # (planned) KPI/metric widgets
│   │   ├── search.py            # (planned) symbol/dataset search
│   │   └── report.py            # (planned) AI report view
│   └── assets/
│       ├── logo.png
│       └── style.css
├── data/
│   ├── download_data.py         # (planned) data acquisition script
│   ├── stock-market-dataset.ipynb  # exploratory notebook
│   └── India_Stock_Market_Data.xlsx # sample dataset
├── requirements.txt
└── .gitignore
```

---

## 🚦 Project Status

**Implemented:**
- ✅ FastAPI backend skeleton with router registration
- ✅ `/market/{symbol}` — live quote lookup via `yfinance`
- ✅ `/upload` — CSV/Excel dataset ingestion, stored in-memory
- ✅ `/profile` — automated dataset profiling (shape, memory usage, missing values, duplicates, dtypes, basic statistics, numeric/categorical column detection, unique value counts)
- ✅ Streamlit app shell with header and module-navigation sidebar

**Scaffolded / not yet implemented:**
- ⬜ Backtesting engine and `/backtest` endpoints
- ⬜ Technical indicators service
- ⬜ ML-based prediction service and `/prediction` endpoints
- ⬜ Analytics endpoints
- ⬜ AI-generated research report service and `/report` endpoints
- ⬜ Streamlit dashboard, charts, metrics, and search components
- ⬜ Application configuration (`settings.py`)
- ⬜ Automated data download script

Contributions toward any of the above are very welcome — see [Contributing](#-contributing).

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/A-PQRP.git
cd A-PQRP
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

### Start the backend (FastAPI)
```bash
uvicorn backend.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

### Start the frontend (Streamlit)
In a separate terminal:
```bash
streamlit run frontend/app.py
```
The dashboard will open at `http://localhost:8501`.

---

## 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check / welcome message |
| `GET` | `/market/{symbol}` | Fetch live market data for a ticker symbol |
| `POST` | `/upload` | Upload a CSV or Excel dataset for analysis |
| `GET` | `/profile` | Get an automated profiling report for the most recently uploaded dataset |

Example: fetching a quote
```bash
curl http://127.0.0.1:8000/market/AAPL
```

Example: uploading a dataset
```bash
curl -F "file=@data/India_Stock_Market_Data.xlsx" http://127.0.0.1:8000/upload
```

---

## 🗺️ Roadmap
- [ ] Technical indicators (moving averages, RSI, MACD, etc.)
- [ ] Strategy backtesting engine with performance metrics
- [ ] ML-based price/trend prediction models
- [ ] AI-generated natural-language research reports
- [ ] Interactive charts and KPI dashboard in Streamlit
- [ ] Persistent storage (replace in-memory dataframe store)
- [ ] User configuration via `settings.py` / environment variables

---

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/backtest-engine`)
3. Commit your changes
4. Open a pull request describing the change

Please open an issue first for larger features so the approach can be discussed.

---

## 📄 License

No license has been specified yet. Add a `LICENSE` file to clarify how others may use this project.

---

## 🙏 Acknowledgements

- Sample dataset sourced from a public stock market dataset on Kaggle
- Market data powered by [yfinance](https://github.com/ranaroussi/yfinance)
<img width="1039" height="700" alt="Screenshot 2026-08-02 at 8 30 18 PM" src="https://github.com/user-attachments/assets/92e34ce4-a084-4a21-aba7-7a27e684a38d" />
<img width="1000" height="491" alt="Screenshot 2026-08-02 at 8 30 05 PM" src="https://github.com/user-attachments/assets/8615c4dd-653a-4106-90db-71c28db522c6" />
<img width="1141" height="459" alt="Screenshot 2026-08-02 at 8 29 46 PM" src="https://github.com/user-attachments/assets/2d22f205-3bd4-40de-a55d-af32a3ec1e2c" />
<img width="1141" height="788" alt="Screenshot 2026-08-02 at 8 29 33 PM" src="https://github.com/user-attachments/assets/061bb216-bbc2-430d-9837-c76365ae0657" />
<img width="1178" height="789" alt="Screenshot 2026-08-02 at 8 29 04 PM" src="https://github.com/user-attachments/assets/adb72896-1f9c-456d-abee-36bacb388d1b" />
<img width="1144" height="744" alt="Screenshot 2026-08-02 at 8 28 51 PM" src="https://github.com/user-attachments/assets/43c022b2-3191-4ecd-8220-c54535514a95" />
<img width="1411" height="749" alt="Screenshot 2026-08-02 at 8 28 38 PM" src="https://github.com/user-attachments/assets/b9b71f3f-99cf-4208-bfea-090645c20f7c" />
<img width="1115" height="613" alt="Screenshot 2026-08-02 at 8 28 22 PM" src="https://github.com/user-attachments/assets/18a86e85-088f-4cdc-bacc-175470e54270" />
<img width="1437" height="644" alt="Screenshot 2026-08-02 at 8 28 12 PM" src="https://github.com/user-attachments/assets/6544b8f2-cb5c-4958-9fd4-b7d61c3962ba" />
<img width="1422" height="794" alt="Screenshot 2026-08-02 at 8 26 57 PM" src="https://github.com/user-attachments/assets/a21439cd-4162-46ac-acba-411da74e0518" />
<img width="1172" height="519" alt="Screenshot 2026-08-02 at 8 26 29 PM" src="https://github.com/user-attachments/assets/8170a0be-d2f7-4299-bab1-57ee73e77bc9" />
<img width="1455" height="749" alt="Screenshot 2026-08-02 at 8 26 05 PM" src="https://github.com/user-attachments/assets/2a37a404-f043-40e8-831a-fddd2cb91bd8" />
