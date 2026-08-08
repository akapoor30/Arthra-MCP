# Arthra MCP — Phase 4 Explanation: Plotly Interactive Visualization Engine

This document provides a detailed technical breakdown of **Phase 4** implementation for **Arthra MCP**, covering the interactive visualization engine built with **Plotly**.

---

## 1. Overview & Components Built

Phase 4 delivers rich, interactive dark-themed visual charts saved as standalone HTML files in `charts/`:
1. `src/visualization/chart_builder.py`: Multi-panel Plotly builder functions for stock candlesticks, indicators, mutual fund NAV trajectories, drawdowns, and relative asset comparison curves vs NIFTY 50.
2. `demo_client/demo_visualization.py`: Interactive client demo executing live visual rendering.
3. `tests/test_visualization.py`: Unit test suite asserting HTML chart rendering and file size integrity.

---

## 2. Interactive Chart Types & Layout Architecture

### A. 3-Panel Stock Technical Candlestick Chart (`build_stock_technical_chart`)
- **Row 1 (60% height)**: Candlestick price chart with volume, Simple Moving Averages (SMA 20, SMA 50, SMA 200), Exponential Moving Averages (EMA 9, EMA 21), and Bollinger Bands fill band.
- **Row 2 (20% height)**: RSI (14) Oscillator with red dashed line at Overbought (70) and green dashed line at Oversold (30).
- **Row 3 (20% height)**: MACD Line, Signal Line, and MACD Histogram (colored green for positive momentum, red for negative).
- **Output File**: `charts/{SYMBOL}_technical.html`

### B. 2-Panel Mutual Fund Performance & Drawdown Chart (`build_mutual_fund_chart`)
- **Row 1 (70% height)**: Historical NAV Growth Trajectory curve with gradient fill and peak annotations.
- **Row 2 (30% height)**: Peak-to-Trough Underwater Drawdown (%) curve highlighting downside risks.
- **Output File**: `charts/MF_{SCHEME_CODE}_performance.html`

### C. Stock Comparison Chart (`build_stock_comparison_chart`)
- Compares multiple Indian stocks (e.g. Reliance, TCS, HDFC Bank) normalized to a $0.0\%$ baseline on day 1 vs NIFTY 50 benchmark (`^NSEI`).
- **Output File**: `charts/stock_comparison.html`

### D. Mutual Fund Comparison Chart (`build_mutual_fund_comparison_chart`)
- Compares multiple Indian Mutual Funds (e.g. Parag Parikh Flexi Cap, SBI Small Cap) normalized over the exact requested period (e.g. 1 Year) vs NIFTY 50 benchmark (`^NSEI`).
- **Output File**: `charts/mf_comparison.html`

---

## 3. Verification & Test Output

All 13 unit tests passed in pytest (`tests/test_visualization.py`, `tests/test_analytics.py`, `tests/test_data_fetchers.py`):
```text
tests/test_analytics.py .... [30%]
tests/test_data_fetchers.py ...... [76%]
tests/test_visualization.py ... [100%]
13 passed in 10.24s
```

Live visual demo (`demo_client/demo_visualization.py`) rendered HTML chart files:
- `charts/RELIANCE_NS_technical.html` (Stock Candlesticks, RSI, MACD, Volume)
- `charts/MF_122640_performance.html` (Parag Parikh Flexi Cap NAV Curve & Drawdown)
- `charts/asset_comparison.html` (Reliance, TCS, HDFC Bank, and PPFC Fund vs NIFTY 50)
