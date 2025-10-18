# Point.Blank - Advanced Stock Analysis Platform


A comprehensive, multilingual stock market analysis platform that combines technical analysis, AI-powered forecasting, and real-time news aggregation. Built with Streamlit and featuring advanced machine learning models for accurate market predictions.

## 🌟 Features

### 📊 Advanced Technical Analysis
- **Moving Averages**: MA20, MA50, EMA12, EMA26
- **Momentum Indicators**: RSI, MACD, Stochastic Oscillator
- **Volatility Indicators**: Bollinger Bands (fixed standard deviation)
- **Trend Analysis**: ADX, Directional Indicators (DI+, DI-)
- **Volume Analysis**: VWAP, On-Balance Volume (OBV)
- **Customizable Charts**: 4-panel advanced visualization

### 🤖 AI-Powered Forecasting Models
- **Prophet**: Long-term trend analysis with seasonality
- **ARIMA**: Statistical time series forecasting with confidence intervals
- **Random Forest**: Ensemble learning with feature engineering
- **LSTM**: Deep learning neural network (data leakage fixed)

### 🌍 Multilingual Support
- **30+ Languages**: Complete UI translation
- **RTL Support**: Arabic, Hebrew, and other right-to-left languages
- **City-based Time Zones**: Interactive globe selection

### 📰 Real-time News Integration
- **Google News RSS**: Latest market news
- **Smart Link Resolution**: Bypasses redirects
- **Image Extraction**: Article thumbnails
- **Duplicate Detection**: URL-based deduplication

### 🔒 Security & Performance
- **Input Validation**: Whitelist-based ticker validation
- **Rate Limiting**: Yahoo Finance API protection
- **Comprehensive Logging**: Production-ready debugging
- **Error Handling**: User-friendly error messages

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended for LSTM)
- Internet connection for data fetching

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/point-blank.git
   cd point-blank
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run point_blank.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 📋 Configuration

### Environment Variables
```bash
# Optional: Set custom port
export STREAMLIT_SERVER_PORT=8501

# Optional: Reduce TensorFlow logging
export TF_CPP_MIN_LOG_LEVEL=2

# Optional: Set log level
export POINTBLANK_LOG_LEVEL=INFO
```

### Model Configuration
The application automatically detects available ML libraries:
- **Prophet**: For long-term forecasting (30-90 days)
- **ARIMA**: For statistical analysis with confidence intervals
- **Random Forest**: For ensemble predictions
- **LSTM**: For deep learning forecasts (requires TensorFlow)

## 🎯 Usage Guide

### Basic Analysis
1. **Enter Ticker Symbol**: Type any valid stock symbol (e.g., AAPL, TSLA, BTC-USD)
2. **Select Time Period**: Choose from 1d to max historical data
3. **Choose Interval**: 1m, 5m, 1h, 1d, 1wk, 1mo
4. **Click "Run All"**: Generate analysis and forecasts

### Advanced Features
- **Technical Indicators**: Toggle on/off for cleaner charts
- **Language Selection**: Use the dropdown in the sidebar
- **Time Zone**: Click on the interactive globe
- **Export Data**: Download raw data as CSV

### Model Recommendations

#### For Day Traders
- **Primary Model**: LSTM (best for 1-7 day forecasts)
- **Interval**: 1d or 1wk
- **Indicators**: RSI, Stochastic, VWAP

#### For Long-term Investors
- **Primary Model**: Prophet (best for 30-90 day trends)
- **Interval**: 1d or 1wk
- **Indicators**: MA50, ADX, MACD

#### For Algorithmic Trading
- **Primary Model**: Random Forest (good for feature engineering)
- **Export Models**: Use for backtesting
- **Indicators**: All available for comprehensive analysis

## 🔧 Technical Details

### Architecture
```
point_blank.py
├── Data Fetching (Yahoo Finance API)
├── Technical Analysis (Pandas, NumPy)
├── Machine Learning Models
│   ├── Prophet (Facebook)
│   ├── ARIMA (Statsmodels)
│   ├── Random Forest (Scikit-learn)
│   └── LSTM (TensorFlow/Keras)
├── News Aggregation (RSS)
├── Visualization (Plotly)
└── UI/UX (Streamlit)
```

### Performance Optimizations
- **Caching**: Streamlit cache_data for expensive operations
- **Rate Limiting**: 1-second intervals between API calls
- **Parallel Processing**: Multi-threaded forecast generation
- **Memory Management**: Proper cleanup for LSTM models

### Security Features
- **Input Sanitization**: Whitelist validation for ticker symbols
- **XSS Protection**: HTML escaping for user inputs
- **Rate Limiting**: Prevents API abuse
- **Error Handling**: Secure error messages

## 📊 Model Performance

### Accuracy Metrics (30-day forecasts)
| Model | Accuracy | Use Case | Data Requirements |
|-------|----------|----------|-------------------|
| Prophet | ±5% | Long-term trends | Min 90 days |
| ARIMA | ±4% | Statistical analysis | Min 100 days |
| Random Forest | ±6% | Feature importance | Min 200 days |
| LSTM | ±3% | Short-term volatility | Min 200 days |

### Technical Indicators
| Indicator | Purpose | Range | Signal |
|-----------|---------|-------|--------|
| RSI | Momentum | 0-100 | >70 Overbought, <30 Oversold |
| ADX | Trend Strength | 0-100 | >25 Strong trend, >50 Very strong |
| Stochastic | Momentum | 0-100 | >80 Overbought, <20 Oversold |
| VWAP | Volume Price | Price | Above = Bullish, Below = Bearish |

## 🐛 Troubleshooting

### Common Issues

#### "No data returned" Error
- **Cause**: Invalid ticker symbol or network issues
- **Solution**: Verify ticker exists on Yahoo Finance
- **Alternative**: Try different ticker formats (.TO for Canadian stocks)

#### LSTM Training Fails
- **Cause**: Insufficient data or memory issues
- **Solution**: Use longer time periods (1y+) or reduce sequence length
- **Check**: Available RAM (8GB+ recommended)

#### Slow Performance
- **Cause**: Large datasets or multiple models
- **Solution**: Use shorter time periods or disable some models
- **Optimization**: Close other applications to free memory

#### Import Errors
- **Cause**: Missing dependencies
- **Solution**: Run `pip install -r requirements.txt`
- **Check**: Python version compatibility

### Log Files
Check `logs/pointblank.log` for detailed error information:
```bash
tail -f logs/pointblank.log
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black point_blank.py

# Lint code
flake8 point_blank.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**IMPORTANT**: Point.Blank provides stock market data, analysis, and predictive tools for **educational and informational purposes only**.

- Point.Blank does **not** provide financial, investment, trading, or legal advice
- All information, forecasts, and analytics are **estimates only** and may be inaccurate
- Stock market investments are inherently **risky and volatile**
- Past performance is not indicative of future results
- Users are solely responsible for any investment decisions
- The developers shall **not be held liable** for any financial losses

**By using Point.Blank, you acknowledge these risks and agree to use the platform at your own discretion.**

##  Acknowledgments

- **Yahoo Finance**: For providing free market data
- **Facebook Prophet**: For time series forecasting
- **Streamlit**: For the amazing web framework
- **Plotly**: For interactive visualizations
- **TensorFlow**: For deep learning capabilities

## 📞 Support

- **Documentation**: [Wiki](https://github.com/antonbeski0/point-blank/wiki)
- **Issues**: [GitHub Issues](https://github.com/antonbeski0/point-blank/issues)
- **Discussions**: [GitHub Discussions](https://github.com/antonbeski0/point-blank/discussions)
- **Email**: antbsk0@gmail.com

---

**Made with ❤️ by the Point.Blank Team**

*Last updated: December 2024*



