# Arthra MCP - Project TODO & Progress Tracker 📝

Track the implementation progress of **Arthra MCP**, synced directly with the phase-wise plan in [docs/plan.md](docs/plan.md).

---

## 📌 Phase 1: Environment & Architecture Setup
- [x] Initialize Python virtual environment (`.venv`) with Python 3.14.
- [x] Create `requirements.txt` with dependencies (`mcp`, `yfinance`, `pandas`, `numpy`, `plotly`, `requests`, `python-dotenv`).
- [x] Create modular project directory structure:
  - `src/data/` (Stock & Mutual Fund fetchers)
  - `src/analytics/` (Quantitative technicals, fundamentals & MF metrics)
  - `src/visualization/` (Plotly chart builder module)
  - `src/mcp_server/` (FastMCP server runner & tool definitions)
  - `src/agent/` (LLM Financial Analyst agent runner)
  - `charts/` (Output interactive HTML charts)
  - `reports/` (Output markdown financial reports)
  - `tests/` (Unit and integration test suites)

---

## 📌 Phase 2: Indian Stock & Mutual Fund Data Ingestion Engine
- [x] **Stock Data Fetcher (`src/data/stock_fetcher.py`)**:
  - [x] Implement ticker symbol normalizer (`RELIANCE` -> `RELIANCE.NS`, `TCS` -> `TCS.NS`).
  - [x] Fetch real-time quotes & historical OHLCV data via `yfinance`.
  - [x] Fetch key fundamental metrics (P/E, P/B, Market Cap, EV/EBITDA, ROE, ROCE, Debt/Equity).
  - [x] Fetch financial statements (Income Statement, Balance Sheet, Cash Flow Statement).
- [x] **Mutual Fund Data Fetcher (`src/data/mf_fetcher.py`)**:
  - [x] Implement scheme search by name via AMFI public API (`mfapi.in`).
  - [x] Parse historical daily NAV series for any Indian Mutual Fund scheme code.
  - [x] Extract scheme metadata (Category, Fund House, Scheme Type).

---

## 📌 Phase 3: Financial Analytics & Quantitative Engine
- [x] **Technical Analysis (`src/analytics/technicals.py`)**:
  - [x] Calculate Moving Averages (Simple SMA 20/50/200, Exponential EMA 9/21).
  - [x] Calculate Relative Strength Index (RSI 14).
  - [x] Calculate MACD (12, 26, 9) line, Signal line & Histogram.
  - [x] Calculate Bollinger Bands (Upper, Middle, Lower, Bandwidth).
  - [x] Compute Volatility & Beta relative to NIFTY 50 (`^NSEI`).
- [x] **Fundamental Scorecard (`src/analytics/fundamentals.py`)**:
  - [x] Valuation analysis (P/E band, P/B, EV/EBITDA vs industry).
  - [x] Profitability & Growth scoring (ROE, ROCE, Margin trends).
  - [x] Financial health score & risk breakdown.
- [x] **Mutual Fund Analytics (`src/analytics/mf_analytics.py`)**:
  - [x] Calculate CAGR for 1-Year, 3-Year, 5-Year, and Since Inception.
  - [x] Calculate Rolling Returns & Volatility (Standard Deviation).
  - [x] Compute Risk Ratios: Sharpe Ratio, Sortino Ratio, Maximum Drawdown.

---

## 📌 Phase 4: Plotly Visualization Engine
- [ ] **Chart Builder (`src/visualization/chart_builder.py`)**:
  - [ ] Build **Stock Candlestick Chart** with Volume, SMA/EMA overlays, RSI & MACD subplots.
  - [ ] Build **Stock Fundamental Trend Charts** (Revenue, Earnings, P/E historical range).
  - [ ] Build **Mutual Fund Performance Chart** (NAV trajectory curve, drawdown plot).
  - [ ] Build **Benchmark Comparison Chart** (Normalize multi-asset returns vs NIFTY 50 on % scale).
  - [ ] Implement HTML chart export into `charts/` with dark/light theme options.

---

## 📌 Phase 5: FastMCP Server Implementation
- [ ] **MCP Tools Definition (`src/mcp_server/tools.py`)**:
  - [ ] `search_indian_symbol`: Resolve Indian stock symbol or mutual fund scheme code.
  - [ ] `fetch_financial_data`: Retrieve raw stock price quotes / mutual fund NAVs / financials.
  - [ ] `analyze_and_visualize`: Run technicals/fundamentals/MF metrics & return Plotly chart URLs.
  - [ ] `compare_assets`: Side-by-side comparative analysis of Indian equities & mutual funds.
- [ ] **FastMCP Server Runner (`src/mcp_server/server.py`)**:
  - [ ] Initialize FastMCP server instance.
  - [ ] Configure STDIO transport protocol.
  - [ ] Add input validation and error handling for invalid symbols or API timeouts.

---

## 📌 Phase 6: Financial Analyst Agent & Interactive Interface
- [ ] **LLM Agent Orchestrator (`src/agent/agent.py`)**:
  - [ ] Build natural language financial analyst agent using registered MCP tools.
  - [ ] Format structured research reports with embedded interactive Plotly chart links.
- [ ] **CLI & Application Entry Point (`main.py`)**:
  - [ ] `--server`: Command flag to launch the FastMCP server for Claude Desktop / Cursor.
  - [ ] `--agent`: Command flag to run interactive CLI financial analyst queries.

---

## 📌 Phase 7: Verification & Documentation
- [ ] Build unit & integration tests (`tests/test_stock_fetcher.py`, `tests/test_mf_fetcher.py`, `tests/test_analytics.py`, `tests/test_mcp_server.py`).
- [ ] Perform live end-to-end verification with Indian stocks (`RELIANCE.NS`, `TCS.NS`) and mutual funds (`Parag Parikh Flexi Cap`).
- [ ] Create `walkthrough.md` with sample outputs, screenshots, and visual verification.
- [ ] Update `README.md` with final installation commands and usage demonstrations.
