
import warnings
warnings.filterwarnings("ignore")

from flask import Flask, jsonify, request, render_template
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import pytz
import feedparser
import urllib.parse
import html
import re
import time
import locale
import json

# Set locale for proper number formatting
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except:
    pass

# --------------------------
# ML libraries
# --------------------------
HAS_PROPHET = False
try:
    from prophet import Prophet
    HAS_PROPHET = True
except ImportError:
    Prophet = None

app = Flask(__name__)

# --------------------------
# Data for new features
# --------------------------
def load_json_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

LANGUAGES = load_json_data('languages.json')
TIMEZONES = load_json_data('timezones.json')
TICKERS = load_json_data('tickers.json')


# --------------------------
# Data fetching and processing functions
# --------------------------
def fetch_yahoo_data(ticker: str, period="6mo", interval="1d", max_retries=3) -> pd.DataFrame:
    """
    Fetch historical market data from Yahoo Finance with retry logic and error handling.
    """
    import time
    from requests.exceptions import RequestException

    m = re.match(r"^([A-Za-z0-9\-\._=]+)", ticker or "")
    clean_ticker = m.group(1) if m else ticker

    if not clean_ticker:
        return pd.DataFrame()

    for attempt in range(max_retries):
        try:
            t = yf.Ticker(clean_ticker)
            df = t.history(period=period, interval=interval)

            if df is None or df.empty:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return pd.DataFrame()

            df = df.reset_index()

            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                try:
                    if df['Date'].dt.tz is not None:
                        df['Date'] = df['Date'].dt.tz_convert(None)
                except Exception:
                    try:
                        df['Date'] = df['Date'].dt.tz_localize(None)
                    except Exception:
                        pass

            numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            required_cols = ['Date', 'Close']
            if not all(col in df.columns for col in required_cols):
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return pd.DataFrame()

            df = df.dropna(subset=['Date', 'Close']).reset_index(drop=True)

            if df.empty:
                return pd.DataFrame()

            return df

        except RequestException as e:
            if attempt == max_retries - 1:
                return pd.DataFrame()
            time.sleep(2 ** attempt)

        except Exception as e:
            if attempt == max_retries - 1:
                return pd.DataFrame()
            time.sleep(2 ** attempt)

    return pd.DataFrame()

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Compute comprehensive technical indicators with proper data leakage prevention"""
    df = df.copy().reset_index(drop=True)

    if len(df) < 50:
        ma_period = min(20, len(df) // 2)
        bb_period = min(20, len(df) // 2)
        rsi_period = min(14, len(df) // 2)
    else:
        ma_period = 20
        bb_period = 20
        rsi_period = 14

    df['MA20'] = df['Close'].rolling(window=ma_period, min_periods=1).mean()
    df['MA50'] = df['Close'].rolling(window=min(50, len(df)), min_periods=1).mean()
    df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['BB_Middle'] = df['Close'].rolling(window=bb_period, min_periods=1).mean()
    df['BB_Std'] = df['Close'].rolling(window=bb_period, min_periods=1).std(ddof=0)
    df['BB_Upper'] = df['BB_Middle'] + (2 * df['BB_Std'])
    df['BB_Lower'] = df['BB_Middle'] - (2 * df['BB_Std'])
    
    delta = df['Close'].diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.ewm(span=rsi_period, adjust=False).mean()
    roll_down = down.ewm(span=rsi_period, adjust=False).mean()
    rs = roll_up / (roll_down + 1e-8)
    df['RSI'] = 100 - (100 / (1 + rs))

    return df

def forecast_prophet(df: pd.DataFrame, periods: int = 30):
    if not HAS_PROPHET or df.empty or len(df) < 20:
        return None
    
    df_prophet = df[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
    
    model = Prophet()
    model.fit(df_prophet)
    
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)


# --------------------------
# News fetching functions
# --------------------------
def get_company_name(ticker: str) -> str:
    if not ticker:
        return ""
    try:
        info = yf.Ticker(ticker).info
        return info.get("shortName") or info.get("longName") or ""
    except Exception:
        return ""

def fetch_google_news(query: str, max_items: int = 8, hl: str = "en-US", gl: str = "US", ceid: str = "US:en"):
    if not query:
        return []
    
    try:
        import requests
        encoded = urllib.parse.quote_plus(query)
        rss_url = f"https://news.google.com/rss/search?q={encoded}&hl={hl}&gl={gl}&ceid={ceid}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(rss_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        feed = feedparser.parse(response.content)
        
        entries = feed.entries or []
        items = []
        for entry in entries:
            items.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
                "source": entry.source.title if hasattr(entry, 'source') and hasattr(entry.source, 'title') else 'N/A'
            })
            if len(items) >= max_items:
                break
        return items
        
    except Exception:
        return []

# --------------------------
# Flask App Routes
# --------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    ticker = request.args.get('ticker')
    period = request.args.get('period', '6mo')
    interval = request.args.get('interval', '1d')

    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    df = fetch_yahoo_data(ticker, period, interval)
    if df.empty:
        return jsonify({"error": "Could not fetch data for the given ticker"}), 404

    df = compute_indicators(df)
    
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    data = df.to_dict(orient='records')
    
    return jsonify({"data": data})

@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    ticker = request.args.get('ticker')
    period = request.args.get('period', '6mo')

    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    df = fetch_yahoo_data(ticker, period, '1d')
    if df.empty:
        return jsonify({"error": "Could not fetch data for the given ticker"}), 404
    
    forecast = forecast_prophet(df)
    if forecast is None:
        return jsonify({"error": "Could not generate forecast"}), 500

    forecast['ds'] = forecast['ds'].dt.strftime('%Y-%m-%d')
    
    return jsonify(forecast.to_dict(orient='records'))

@app.route('/api/news', methods=['GET'])
def get_news():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    company_name = get_company_name(ticker)
    query = f'{ticker} OR "{company_name}"' if company_name else ticker
    
    articles = fetch_google_news(query, max_items=10)
    
    return jsonify(articles)

@app.route('/api/search_tickers', methods=['GET'])
def search_tickers():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])

    results = [
        {"ticker": t, "name": n}
        for t, n in TICKERS.items()
        if query in t.lower() or query in n.lower()
    ]
    return jsonify(results)

@app.route('/api/languages', methods=['GET'])
def get_languages():
    return jsonify(LANGUAGES)

@app.route('/api/timezones', methods=['GET'])
def get_timezones():
    return jsonify(TIMEZONES)

if __name__ == '__main__':
    app.run(debug=True)
