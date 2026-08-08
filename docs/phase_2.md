# Arthra MCP — Phase 2 Explanation: Indian Market Data Ingestion Engine

This document provides a detailed breakdown of **Phase 2** implementation, covering data ingestion for **Indian Equity Stocks (NSE/BSE)** and **Indian Mutual Funds (AMFI)**.

---

## 1. Overview & Components Built

In Phase 2, we built two core data ingestion modules:
1. `src/data/stock_fetcher.py`: Interacts with Yahoo Finance (`yfinance`) to fetch quotes, historical OHLCV data, fundamentals, and financial statements for Indian equities.
2. `src/data/mf_fetcher.py`: Interacts with the AMFI REST API (`mfapi.in`) to search schemes, fetch scheme details, and parse historical NAV time-series for Indian Mutual Funds.

---

## 2. Stock Data Ingestion (`src/data/stock_fetcher.py`)

### Ticker Symbol Normalization
Indian stocks traded on National Stock Exchange (NSE) use `.NS` extensions (e.g., `RELIANCE.NS`, `TCS.NS`), while Bombay Stock Exchange (BSE) stocks use `.BO` extensions or BSE scrip codes (e.g., `500325.BO`).

Function `normalize_indian_symbol(symbol: str)` ensures:
- Input `RELIANCE` -> `RELIANCE.NS`
- Input `TCS.NS` -> `TCS.NS`
- Automatic fallback retry logic to `.BO` if an exchange ticker returns empty info.

### Key Ingestion Functions

| Function Name | Return Type | Description |
| :--- | :--- | :--- |
| `normalize_indian_symbol(symbol)` | `str` | Appends `.NS` suffix default to bare Indian stock tickers. |
| `get_stock_quote(symbol)` | `Dict[str, Any]` | Real-time quote: Current Price, Open, High, Low, Previous Close, Volume, Market Cap, 52-Week High/Low. |
| `get_historical_ohlcv(symbol, period, interval)` | `pd.DataFrame` | Cleaned time-series OHLCV DataFrame with columns `['Open', 'High', 'Low', 'Close', 'Volume']`. |
| `get_stock_fundamentals(symbol)` | `Dict[str, Any]` | Valuation ratios (P/E, P/B, EV/EBITDA, Beta, Dividend Yield, ROE, ROCE, Debt/Equity). |
| `get_financial_statements(symbol)` | `Dict[str, Any]` | Annual & Quarterly Income Statements, Balance Sheets, Cash Flow Statements. |

---

## 3. Mutual Fund Data Ingestion (`src/data/mf_fetcher.py`)

### AMFI REST API Integration
Indian Mutual Fund scheme NAVs are published daily by the Association of Mutual Funds in India (AMFI). We fetch them via the high-speed public endpoint `https://api.mfapi.in/mf`.

### Key Ingestion Functions

| Function Name | Return Type | Description |
| :--- | :--- | :--- |
| `search_mutual_fund(query)` | `List[Dict]` | Searches scheme codes and names matching a keyword (e.g., `"Parag Parikh Flexi Cap"`). |
| `get_mutual_fund_details(scheme_code)` | `Dict[str, Any]` | Scheme metadata (Fund House, Category, Type, Latest NAV, Latest Date). |
| `get_mutual_fund_nav_df(scheme_code)` | `pd.DataFrame` | Historical NAV DataFrame sorted chronologically (oldest to newest date) with datetime index. |

---

## 4. Verification & Testing

Automated test suite created in `tests/test_data_fetchers.py`:
- `test_symbol_normalization`: Verifies `.NS` / `.BO` symbol parsing.
- `test_get_stock_quote`: Verifies live quotes for `RELIANCE.NS`.
- `test_get_historical_ohlcv`: Verifies 1-month daily OHLCV DataFrame structure for `TCS.NS`.
- `test_get_stock_fundamentals`: Verifies valuation metrics for `HDFCBANK.NS`.
- `test_search_mutual_fund`: Verifies search results for `"Parag Parikh"`.
- `test_get_mutual_fund_details_and_df`: Verifies scheme details & NAV series for `Parag Parikh Flexi Cap Fund`.

**Execution Output**:
```text
tests/test_data_fetchers.py ...... [100%]
6 passed in 3.42s
```
