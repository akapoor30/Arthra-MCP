# Arthra MCP: Indian Stock & Mutual Fund Financial Analyst System

Build **Arthra MCP** — an automated, local **Financial Analyst System powered by Model Context Protocol (MCP)** tailored specifically for **Indian Equity (NSE/BSE)** and **Indian Mutual Funds (AMFI)**.

The architecture follows the user workflow model: an **LLM Agent** invoking **MCP Tools** backed by financial data APIs (`yfinance`, `mfapi.in`), quantitative computation engines (`NumPy`, `Pandas`), and interactive visualization engines (`Plotly`).

---

## 1. High-Level Architecture Flow

```mermaid
flowchart TD
    User["User Query<br/>('Analyze RELIANCE & PPFC Fund')"] --> Agent["LLM Agent / Financial Analyst Client"]
    Agent <-->|MCP JSON-RPC Protocol| MCPServer["FastMCP Financial Analyst Server"]

    subgraph ServerCore["MCP Server Core Engine"]
        MCPServer --> DataEngine["Data Fetcher Module<br/>(yfinance NSE/BSE + mfapi.in MFs)"]
        MCPServer --> QuantEngine["Analytics & Computation Engine<br/>(NumPy + Pandas Financial Ratios)"]
        MCPServer --> VisEngine["Plotly Visualization Engine<br/>(Candlestick, RSI, MACD, NAV Curves)"]
    end

    DataEngine <-->|REST API| NSE["NSE / BSE (yfinance)"]
    DataEngine <-->|REST API| AMFI["Indian Mutual Funds (mfapi.in)"]

    MCPServer --> Deliverables["Structured Markdown Report + Plotly Charts"]
    Deliverables --> Agent
```

---

## 2A. Stock Analysis Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Investor
    participant Agent as LLM Agent
    participant MCP as FastMCP Server
    participant Data as Stock Fetcher
    participant Quant as NumPy/Pandas
    participant Vis as Plotly Builder

    User->>Agent: "Analyze RELIANCE stock"
    Agent->>MCP: 1. search_indian_symbol("RELIANCE")
    MCP-->>Agent: RELIANCE.NS (NSE Equity)

    Agent->>MCP: 2. fetch_financial_data(symbol="RELIANCE.NS")
    MCP->>Data: Fetch OHLCV & Fundamentals (yfinance)
    Data-->>MCP: Stock Quotes & Financial Statements
    MCP-->>Agent: Raw Market Data

    Agent->>MCP: 3. analyze_and_visualize(symbol="RELIANCE.NS", metrics=["technicals", "chart"])
    MCP->>Quant: Compute SMA, EMA, RSI, MACD, Volatility
    Quant-->>MCP: Technical Indicators
    MCP->>Vis: Render Candlestick & Technical Plotly HTML Chart
    Vis-->>MCP: Saved chart to charts/RELIANCE_NS.html
    MCP-->>Agent: Indicator Ratios + Interactive Chart URL

    Agent->>User: Stock Report + Interactive Plotly Chart
```

---

## 2B. Mutual Fund Analysis Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Investor
    participant Agent as LLM Agent
    participant MCP as FastMCP Server
    participant Data as MF Fetcher
    participant Quant as NumPy/Pandas
    participant Vis as Plotly Builder

    User->>Agent: "Analyze Parag Parikh Flexi Cap Fund"
    Agent->>MCP: 1. search_indian_symbol("Parag Parikh")
    MCP-->>Agent: Scheme Code: 122639

    Agent->>MCP: 2. fetch_financial_data(symbol="122639", type="mutual_fund")
    MCP->>Data: Fetch NAV History & Category Info (mfapi.in)
    Data-->>MCP: Historical Scheme NAVs
    MCP-->>Agent: Scheme NAV Data

    Agent->>MCP: 3. analyze_and_visualize(symbol="122639", metrics=["mf_returns", "drawdown"])
    MCP->>Quant: Compute CAGR (1Y/3Y/5Y), Sharpe, Max Drawdown
    Quant-->>MCP: Risk & Return Ratios
    MCP->>Vis: Render NAV Trajectory & Drawdown Plotly HTML Chart
    Vis-->>MCP: Saved chart to charts/MF_122639.html
    MCP-->>Agent: MF Performance + Interactive Chart URL

    Agent->>User: Mutual Fund Report + Interactive Plotly Chart
```

---

## 3. Modular System Architecture

```mermaid
graph LR
    subgraph DataFetcher["src/data"]
        SF["stock_fetcher.py<br/>(yfinance ticker resolution)"]
        MF["mf_fetcher.py<br/>(mfapi.in scheme parser)"]
    end

    subgraph Analytics["src/analytics"]
        TA["technicals.py<br/>(SMA, EMA, RSI, MACD, Beta)"]
        FA["fundamentals.py<br/>(P/E, P/B, ROE, ROCE)"]
        MFA["mf_analytics.py<br/>(CAGR, XIRR, Sharpe, Drawdowns)"]
    end

    subgraph Visualization["src/visualization"]
        CB["chart_builder.py<br/>(Plotly Candlesticks, Subplots, NAV Curves)"]
    end

    subgraph MCPServer["src/mcp_server"]
        ST["tools.py<br/>(MCP Tool Definitions)"]
        SRV["server.py<br/>(FastMCP Server Runner)"]
    end

    subgraph AgentClient["src/agent"]
        AG["agent.py<br/>(Financial Analyst Agent)"]
    end

    SF --> TA
    SF --> FA
    MF --> MFA
    TA --> CB
    FA --> CB
    MFA --> CB

    TA --> ST
    FA --> ST
    MFA --> ST
    CB --> ST
    ST --> SRV
    SRV <--> AG
```

---

## 4. Phase-Wise Execution Roadmap

```mermaid
timeline
    title Indian Stock & MF Financial Analyst Roadmap
    Phase 1 : Environment Setup : Python 3.14 venv : Install mcp, yfinance, pandas, numpy, plotly : Create folder structure
    Phase 2 : Data Ingestion : Stock Fetcher (.NS / .BO resolution) : Mutual Fund Fetcher (mfapi.in API) : Caching & rate limiting
    Phase 3 : Quantitative Engine : Technical Indicators (RSI, MACD, SMA/EMA) : Fundamental Scorecard (P/E, ROE) : Mutual Fund Risk Metrics (CAGR, Sharpe, Drawdown)
    Phase 4 : Plotly Visualization : Interactive Stock Candlestick Chart : Fundamental Trend Charts : Mutual Fund NAV Trajectory & Drawdowns : Benchmark Comparison vs NIFTY 50
    Phase 5 : FastMCP Server : Register Core MCP Tools : JSON-RPC interface over STDIO : Error handling & input sanitization
    Phase 6 : Agent & Interface : Intelligent LLM Financial Analyst Agent : Automated report synthesis : CLI & Interactive runner
    Phase 7 : Verification : Unit & Integration Tests : Real-world verification (RELIANCE, PPFC Fund) : Documentation & Walkthrough
```

---

## Technical Highlights
- **Data Source**: Stocks via `yfinance` with `.NS` (NSE) and `.BO` (BSE) ticker extensions (e.g. `RELIANCE.NS`, `TCS.NS`, `HDFCBANK.NS`). Mutual Funds via free public AMFI API (`mfapi.in`) for all Indian Mutual Fund scheme NAVs & historical performance.
- **Protocol**: Built using official Python `mcp` / `FastMCP` framework for seamless integration with Claude Desktop, Cursor, Custom LLM Agents, or CLI clients.
- **Visuals**: Interactive Plotly Candlestick charts, Technical Indicators (RSI, MACD, Moving Averages, Bollinger Bands), Mutual Fund NAV performance curves, and asset comparison charts.

---

## Phase Breakdown & File Mapping

### Phase 1: Environment & Architecture Setup
- Initialize Python virtual environment (`.venv`).
- Install core packages: `mcp`, `yfinance`, `pandas`, `numpy`, `plotly`, `requests`, `python-dotenv`.
- Set up directory structure:
  - `src/data/`: Stock & Mutual Fund data fetchers
  - `src/analytics/`: Technical, fundamental & mutual fund metrics engines
  - `src/visualization/`: Plotly chart builder module
  - `src/mcp_server/`: FastMCP server implementation & tool definitions
  - `src/agent/`: LLM Financial Analyst agent runner & prompt interface
  - `reports/` & `charts/`: Output directory for generated reports and visual HTML charts

### Phase 2: Indian Stock & Mutual Fund Data Ingestion Engine
- Implement `src/data/stock_fetcher.py`:
  - NSE/BSE ticker resolver (`RELIANCE` -> `RELIANCE.NS`).
  - Historical OHLCV, real-time quote, valuation ratios, balance sheet, income statement, cash flow statement.
- Implement `src/data/mf_fetcher.py`:
  - Scheme search by name via `mfapi.in` (e.g., "Parag Parikh Flexi Cap").
  - NAV history fetcher & scheme metadata extraction (Category, Fund House).

### Phase 3: Financial Analytics & Quantitative Engine
- Implement `src/analytics/technicals.py`:
  - Moving Averages (SMA 20/50/200, EMA 9/21).
  - RSI (14), MACD (12, 26, 9), Bollinger Bands.
  - Beta calculation relative to NIFTY 50 (`^NSEI`).
- Implement `src/analytics/fundamentals.py`:
  - Valuation metrics (P/E, P/B, EV/EBITDA), profitability (ROE, ROCE), financial strength score.
- Implement `src/analytics/mf_analytics.py`:
  - CAGR (1Y, 3Y, 5Y, Since Inception), Rolling Returns, Volatility, Sharpe Ratio, Sortino Ratio, Maximum Drawdown.

### Phase 4: Plotly Visualization Engine
- Implement `src/visualization/chart_builder.py`:
  - Stock Candlestick chart with volume, SMA/EMA overlays, RSI & MACD subplots.
  - Stock fundamental trend charts (Revenue, Earnings, P/E band).
  - Mutual Fund NAV trajectory & drawdown plots.
  - Multi-asset relative return comparison chart against NIFTY 50 benchmark.
  - Interactive HTML file export & display.

### Phase 5: MCP Server Implementation (FastMCP)
- Implement `src/mcp_server/server.py` & `src/mcp_server/tools.py`:
  - Register tools:
    1. `search_indian_symbol`: Resolve stock ticker or mutual fund scheme code.
    2. `fetch_financial_data`: Pull stock prices / mutual fund NAVs / financials.
    3. `analyze_and_visualize`: Run calculations (technicals, rolling averages, CAGR, Sharpe) and generate Plotly charts.
    4. `compare_assets`: Side-by-side performance comparison of Indian stocks/MFs.

### Phase 6: Financial Analyst Agent & Interactive Interface
- Implement `src/agent/agent.py`:
  - Intelligent financial agent using MCP tools.
  - Formats natural language questions into structured tools calls and synthesizes comprehensive research reports with embedded Plotly charts.
- Implement `main.py`: Main CLI entry point to launch MCP server or run agent commands.

### Phase 7: Testing, Verification & Walkthrough
- Test suite with real Indian stock symbols (`RELIANCE.NS`, `TCS.NS`) and mutual funds (`Parag Parikh Flexi Cap`).
- Generate sample reports and HTML chart artifacts.
- Create user documentation in `README.md` and complete project walkthrough.
