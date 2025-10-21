# POINT.BLANK
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

**Point.Blank** — a polished Streamlit app for stock market data, technical analysis, news aggregation, and multiple forecasting models (Prophet, ARIMA, Random Forest, LSTM). It’s designed for interactive exploration, quick exports (CSV/JSON), and optional ML-powered forecasting when the appropriate libraries are installed.

---

## Table of Contents
- [Key Features](#key-features)  
- [IMAGES](#IMAGES)  
- [Requirements](#requirements)  
- [Installation](#installation)  
- [Quick Start](#quick-start)  
- [Configuration & Options](#configuration--options)  
- [Models & Optional Dependencies](#models--optional-dependencies)  
- [Internals & Important Notes](#internals--important-notes)  
- [Contributing](#contributing)  
- [License](#license)  
- [Authors & Contact](#authors--contact)  
- [Disclaimer](#disclaimer)

---

## Key Features
- Fetch historical market data from Yahoo Finance (via `yfinance`) with retry/validation logic.  
- Interactive, high-fidelity price charts and technical indicators (SMA, MACD, RSI, Bollinger Bands, ATR, etc.).  
- Technical-analysis summary and signal metrics (Overall Signal, Technical Score, Price Trend).  
- News aggregation (RSS parsing + deduplication) and export to CSV.  
- Multiple forecasting engines:
  - **Prophet** — time series forecasting with regressors.  
  - **ARIMA** — stationarity checks and automatic order selection.  
  - **Random Forest** — feature engineering + lagged features for regression.  
  - **LSTM (TensorFlow)** — enhanced LSTM forecasting when dataset size permits.

---

## IMAGES
<img width="744" height="496" alt="5" src="https://github.com/user-attachments/assets/557f11f6-f580-4480-9594-bd7c53370c4e" />
<img width="508" height="304" alt="4" src="https://github.com/user-attachments/assets/8cc0fa52-7824-4ffd-bb4e-72452b6a081c" />


---

## Requirements

Minimum (core) Python packages:
- Python 3.9+ (recommended)
- `streamlit`
- `yfinance`
- `pandas`
- `numpy`
- `plotly`
- `streamlit-plotly-events`
- `feedparser`
- `pytz`
- `requests`

Optional (for forecasting / advanced features):
- `prophet`
- `statsmodels`, `pmdarima`
- `scikit-learn`
- `tensorflow`

---

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

2. (Recommended) Create and activate a virtual environment:
```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

3. Install the core dependencies:
```bash
pip install streamlit yfinance pandas numpy plotly streamlit-plotly-events feedparser pytz requests
```

4. Install optional ML dependencies when you need them:
```bash
pip install prophet statsmodels pmdarima scikit-learn tensorflow
```

---

## Quick Start

1. Rename your file to `point_blank.py` (if needed).
2. Run the app:
```bash
streamlit run point_blank.py
```
3. In the browser UI:
- Accept the disclaimer to continue.  
- Select a ticker (e.g., `AAPL`, `TSLA`, `BTC-USD`).  
- Choose history period, enable indicators, then press **Run All**.

---

## Configuration & Options

- **Ticker validation** before fetching.  
- **Model detection** for optional ML dependencies.  
- **Export options** for data and news (CSV/JSON).  

---

## Models & Optional Dependencies

- **Prophet** — regression-based time series forecasting.  
- **ARIMA** — automatic order selection for stationarity.  
- **Random Forest** — predictive model using lagged features.  
- **LSTM (TensorFlow)** — deep-learning model for sequence prediction.

---

## Internals & Architecture Notes

- `fetch_yahoo_data()` — robust data fetcher.  
- `compute_indicators()` — SMA, MACD, RSI, Bollinger Bands.  
- `generate_technical_analysis()` — human-readable summary.  

---

## Contributing

1. Fork the repo.  
2. Create a branch: `git checkout -b feat/your-feature`.  
3. Commit and open a PR.  
4. Include tests for new functionality.

---

## License

This project is licensed under the **MIT License**. See `LICENSE` for details.

---

## Authors & Contact

- **Anton Beski.M**  
- For support or feedback, open an issue or PR.

---

## Disclaimer

Point.Blank provides market data and forecasts **for educational purposes only**.  
It does **not** offer financial or investment advice.
