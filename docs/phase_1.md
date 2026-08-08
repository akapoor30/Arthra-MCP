# Arthra MCP — Phase 1 Explanation: Environment Setup & Architecture Foundation

This document provides a comprehensive breakdown of **Phase 1** implementation for **Arthra MCP**.

---

## 1. Objective
Establish an isolated Python runtime environment (`.venv`), configure dependencies for financial data fetching, quantitative analysis, visualization, and FastMCP protocol integration, and build a modular package structure.

---

## 2. Architecture & Directory Layout

```text
mcp_financal_analyst/
├── .venv/                   # Python 3.14 Virtual Environment
├── requirements.txt         # Production Dependency Lockfile
├── src/                     # Core Python Package (`src`)
│   ├── __init__.py          # Package Initialization (v0.1.0)
│   ├── data/                # Data Ingestion Engine (yfinance & mfapi)
│   │   └── __init__.py
│   ├── analytics/           # Quantitative Engine (TA, FA, MF Metrics)
│   │   └── __init__.py
│   ├── visualization/       # Plotly Interactive Chart Builder
│   │   └── __init__.py
│   ├── mcp_server/          # FastMCP Server & Tools Implementation
│   │   └── __init__.py
│   └── agent/               # Financial Analyst LLM Agent Interface
│       └── __init__.py
├── charts/                  # Storage for generated interactive Plotly HTML charts
├── reports/                 # Storage for generated markdown financial reports
├── tests/                   # Automated unit & integration test suites
│   └── __init__.py
└── docs/                    # Phase Explanations & Technical Architecture
    ├── info.txt
    ├── plan.md
    ├── phase_1.md
    └── phase_2.md
```

---

## 3. Dependencies Installed & Rationale

| Library | Version | Purpose & Rationale |
| :--- | :--- | :--- |
| `mcp` | `>=2.0.0` | Official Model Context Protocol SDK (`FastMCP`) for defining JSON-RPC tools and server endpoints. |
| `yfinance` | `>=1.5.0` | Ingest real-time quotes, OHLCV candle history, balance sheets, income statements, and valuation ratios for Indian stocks (`.NS` / `.BO`). |
| `requests` | `>=2.34.0` | REST client to query AMFI public API (`mfapi.in`) for Indian Mutual Fund scheme NAV histories. |
| `pandas` | `>=3.0.0` | Time-series DataFrame management for stock candles and mutual fund NAV series. |
| `numpy` | `>=2.5.0` | High-performance mathematical computations for SMA, EMA, RSI, MACD, Sharpe Ratio, Sortino Ratio, and Max Drawdown. |
| `plotly` | `>=6.9.0` | Interactive HTML candlestick charting, technical subplots, NAV growth curves, and multi-asset performance comparisons. |
| `kaleido` | `>=1.3.0` | Export Plotly interactive charts to high-resolution static PNG/SVG images for reports. |
| `python-dotenv` | `>=1.2.0` | Environment variable management for API keys and host configurations. |

---

## 4. Verification Execution
Phase 1 verification script executed inside `.venv`:
```bash
.venv/bin/python3 -c "import mcp, yfinance, pandas, numpy, plotly, requests; print('✅ Phase 1 Verification Success!')"
```
**Result**: All core packages installed and imported cleanly without syntax or platform binary errors.
