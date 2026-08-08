# Arthra MCP — Phase 3 Explanation: Quantitative & Financial Analytics Engine

This document provides a detailed technical breakdown of **Phase 3** implementation for **Arthra MCP**, covering quantitative technical indicators, fundamental scorecard models, and mutual fund risk-adjusted performance calculations.

---

## 1. Overview & Modules Built

Phase 3 introduces the mathematical core of Arthra MCP:
1. `src/analytics/technicals.py`: Quantitative technical indicator calculations (SMA, EMA, RSI, MACD, Bollinger Bands, Beta vs NIFTY 50) and bullish/bearish signal evaluation.
2. `src/analytics/fundamentals.py`: Financial health scorecard (100-point rating system), valuation assessment (P/E, P/B), profitability scoring (ROE, ROCE), and debt/liquidity ratios.
3. `src/analytics/mf_analytics.py`: Mutual fund performance analytics (CAGR 1Y/3Y/5Y/Inception, 1-Year Rolling Returns, Volatility, Sharpe Ratio, Sortino Ratio, Maximum Drawdown).

---

## 2. Technical Analysis Module (`src/analytics/technicals.py`)

### Mathematical Formulas Implemented

#### Simple & Exponential Moving Averages (SMA / EMA)
$$\text{SMA}_n = \frac{1}{n} \sum_{i=0}^{n-1} P_{t-i}$$

$$\text{EMA}_t = \alpha \cdot P_t + (1 - \alpha) \cdot \text{EMA}_{t-1}, \quad \alpha = \frac{2}{N + 1}$$

#### Relative Strength Index (RSI 14)
Uses Wilder's Exponential Moving Average:
$$\text{RSI} = 100 - \left( \frac{100}{1 + \text{RS}} \right), \quad \text{RS} = \frac{\text{EMA}_{14}(\text{Gain})}{\text{EMA}_{14}(\text{Loss})}$$

#### MACD & Bollinger Bands
- **MACD Line**: $\text{EMA}_{12}(\text{Close}) - \text{EMA}_{26}(\text{Close})$
- **Signal Line**: $\text{EMA}_9(\text{MACD Line})$
- **Bollinger Bands**: $\text{SMA}_{20} \pm (2 \cdot \sigma_{20})$

#### Beta relative to NIFTY 50 (`^NSEI`)
$$\beta = \frac{\text{Covariance}(R_{\text{stock}}, R_{\text{Nifty}})}{\text{Variance}(R_{\text{Nifty}})}$$

---

## 3. Fundamental Health Scorecard (`src/analytics/fundamentals.py`)

100-Point Scoring Model across 4 Financial Pillars:
- **Valuation Pillar (25 pts)**: P/E < 20 (+25 pts), P/E 20-35 (+18 pts), P/E > 35 (+10 pts).
- **Profitability Pillar (25 pts)**: ROE $\ge$ 18% (+25 pts), ROE $\ge$ 12% (+18 pts), ROE < 12% (+10 pts).
- **Growth Pillar (25 pts)**: Positive Revenue Growth (+12.5 pts) & Earnings Growth (+12.5 pts).
- **Solvency & Debt Pillar (25 pts)**: Debt/Equity < 0.5 (+25 pts), D/E 0.5-1.0 (+18 pts), D/E > 1.0 (+8 pts).

---

## 4. Mutual Fund Quantitative Analytics (`src/analytics/mf_analytics.py`)

### Compound Annual Growth Rate (CAGR)
$$\text{CAGR} = \left( \frac{\text{NAV}_{\text{end}}}{\text{NAV}_{\text{start}}} \right)^{\frac{1}{\text{Years}}} - 1$$

### Risk-Adjusted Ratios (Sharpe & Sortino)
$$\text{Sharpe Ratio} = \frac{R_p - R_f}{\sigma_p}$$
*where $R_f = 6.5\%$ (RBI 91-day T-Bill rate) and $\sigma_p$ is annualized volatility.*

$$\text{Sortino Ratio} = \frac{R_p - R_f}{\sigma_{\text{downside}}}$$

### Maximum Drawdown (MDD)
$$\text{MDD} = \min_{t} \left( \frac{\text{NAV}_t - \max_{s \le t} \text{NAV}_s}{\max_{s \le t} \text{NAV}_s} \right)$$

---

## 5. Verification & Test Output

All 10 unit tests executed cleanly via pytest (`tests/test_analytics.py` and `tests/test_data_fetchers.py`):
```text
tests/test_analytics.py .... [40%]
tests/test_data_fetchers.py ...... [100%]
10 passed in 4.38s
```

Live Demo execution (`demo_analytics.py`) results:
- **TCS.NS**: Technical Sentiment = **BULLISH**, RSI = 63.37, Beta vs NIFTY 50 = **0.85**, Fundamental Score = **100/100**.
- **SBI Small Cap Fund (125497)**: 12.72 Years Analyzed, CAGR Since Inception = **24.48%**, Sharpe Ratio = **0.45**, Max Drawdown = **-40.26%**, 1-Year Rolling Return Avg = **26.49%**.
