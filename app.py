"""
Arthra MCP — Interactive Streamlit Web Dashboard UI.
AI-Powered Financial Analyst Dashboard for Indian Equities (NSE/BSE) and Mutual Funds (AMFI).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath("."))

from src.data.stock_fetcher import (
    normalize_indian_symbol,
    get_stock_quote,
    get_historical_ohlcv,
    get_stock_fundamentals,
)
from src.data.mf_fetcher import (
    search_mutual_fund,
    get_mutual_fund_details,
    get_mutual_fund_nav_df,
)
from src.analytics.technicals import (
    get_full_technical_analysis,
    calculate_beta_and_volatility,
    calculate_sma,
    calculate_ema,
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands,
)
from src.analytics.fundamentals import compute_financial_health_scorecard
from src.analytics.mf_analytics import analyze_mutual_fund_performance
from src.agent.agent import FinancialAnalystAgent

# Streamlit Page Config
st.set_page_config(
    page_title="Arthra MCP — Financial Analyst Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS Styling
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .metric-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 1.2rem;
        border: 1px solid #2a2e39;
        margin-bottom: 1rem;
    }
    .score-badge {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00e676;
    }
    .badge-bullish {
        background-color: #1b5e20;
        color: #81c784;
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
    }
    .badge-bearish {
        background-color: #b71c1c;
        color: #ef9a9a;
        padding: 0.3rem 0.8rem;
        border-radius: 6px;
        font-weight: 600;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar
if os.path.exists("images/image.png"):
    st.sidebar.image("images/image.png", use_container_width=True)
st.sidebar.title("📈 Arthra MCP Navigation")
mode = st.sidebar.radio(
    "Select Feature Module:",
    [
        "📊 Indian Equity Analysis",
        "🏦 Mutual Fund Analysis",
        "⚡ Multi-Asset Comparison",
        "🏢 Stock Peer Comparison Matrix",
        "🤖 AI Financial Agent",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Arthra MCP v0.1.0**\nPowered by Model Context Protocol, yfinance, & AMFI REST API."
)


# ==========================================
# MODULE 1: INDIAN EQUITY STOCK ANALYSIS
# ==========================================
if mode == "📊 Indian Equity Analysis":
    st.markdown(
        '<div class="main-header">📈 Indian Equity Stock Analysis (NSE / BSE)</div>',
        unsafe_allow_html=True,
    )

    col_search, col_period = st.columns([3, 1])
    with col_search:
        ticker_input = st.text_input(
            "Enter Indian Stock Symbol or Name (e.g. RELIANCE, TCS, HDFCBANK, INFY):",
            value="RELIANCE",
        )
    with col_period:
        period_input = st.selectbox(
            "Select Time Period:", ["3mo", "6mo", "1y", "2y", "5y"], index=2
        )

    if ticker_input:
        symbol = normalize_indian_symbol(ticker_input)
        with st.spinner(f"Fetching live market data for {symbol}..."):
            try:
                quote = get_stock_quote(symbol)
                df_ohlcv = get_historical_ohlcv(symbol, period=period_input)
                fundamentals = get_stock_fundamentals(symbol)
                scorecard = compute_financial_health_scorecard(fundamentals)
                ta_results = get_full_technical_analysis(df_ohlcv)
                beta_results = calculate_beta_and_volatility(df_ohlcv)

                # Header Metrics Row
                m1, m2, m3, m4, m5 = st.columns(5)
                m1.metric("Current Price", f"₹{quote.get('currentPrice', 0):,.2f}", f"{quote.get('percentChange', 0):+.2f}%")
                m2.metric("52-Week High", f"₹{quote.get('fiftyTwoWeekHigh', 0):,.2f}")
                m3.metric("52-Week Low", f"₹{quote.get('fiftyTwoWeekLow', 0):,.2f}")
                m4.metric("Market Cap (Cr)", f"₹{(quote.get('marketCap', 0) or 0) / 10**7:,.0f} Cr")
                m5.metric("Technical Sentiment", ta_results.get("overallSentiment", "NEUTRAL"))

                st.markdown("---")

                # Columns for Scorecard & Technical Highlights
                col_sc, col_ta = st.columns([1, 1])

                with col_sc:
                    st.subheader("🧮 100-Point Financial Health Scorecard")
                    score = scorecard.get("healthScore", 0)
                    st.progress(score / 100.0)
                    st.markdown(f"**Score**: `{score} / 100` — **{scorecard.get('scoreRating')}**")
                    st.markdown(f"**Valuation Status**: `{scorecard.get('valuationStatus')}`")
                    
                    st.markdown("##### Scorecard Breakdown:")
                    for bd in scorecard.get("scoreBreakdown", []):
                        st.markdown(f"- {bd}")

                with col_ta:
                    st.subheader("📈 Quantitative Technical Signals")
                    st.markdown(f"**RSI (14)**: `{ta_results.get('rsi')}`")
                    st.markdown(f"**Annualized Volatility**: `{beta_results.get('volatility')}%`")
                    st.markdown(f"**Beta vs NIFTY 50**: `{beta_results.get('beta')}`")
                    
                    st.markdown("##### Signal Highlights:")
                    for sig in ta_results.get("signalHighlights", []):
                        st.markdown(f"- {sig}")

                st.markdown("---")

                # Interactive Plotly Candlestick Chart
                st.subheader("📊 Interactive Plotly Candlestick & Indicator Chart")
                
                # Build Plotly Figure
                fig = make_subplots(
                    rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.04,
                    row_heights=[0.60, 0.20, 0.20],
                    subplot_titles=(
                        f"<b>{symbol}</b> Price & Moving Averages",
                        "<b>RSI (14)</b> Oscillator",
                        "<b>MACD</b> Momentum"
                    )
                )

                # Row 1: Candlestick
                fig.add_trace(
                    go.Candlestick(
                        x=df_ohlcv.index, open=df_ohlcv["Open"], high=df_ohlcv["High"],
                        low=df_ohlcv["Low"], close=df_ohlcv["Close"], name="OHLC Price"
                    ), row=1, col=1
                )
                fig.add_trace(go.Scatter(x=df_ohlcv.index, y=calculate_sma(df_ohlcv, 20), name="SMA 20", line=dict(color="#29b6f6")), row=1, col=1)
                fig.add_trace(go.Scatter(x=df_ohlcv.index, y=calculate_sma(df_ohlcv, 50), name="SMA 50", line=dict(color="#ab47bc")), row=1, col=1)
                fig.add_trace(go.Scatter(x=df_ohlcv.index, y=calculate_ema(df_ohlcv, 9), name="EMA 9", line=dict(color="#26c6da", dash="dot")), row=1, col=1)

                # Row 2: RSI
                rsi_series = calculate_rsi(df_ohlcv, 14)
                fig.add_trace(go.Scatter(x=df_ohlcv.index, y=rsi_series, name="RSI 14", line=dict(color="#ab47bc")), row=2, col=1)
                fig.add_hline(y=70, line_dash="dash", line_color="#ef5350", row=2, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="#26a69a", row=2, col=1)

                # Row 3: MACD
                macd_d = calculate_macd(df_ohlcv)
                fig.add_trace(go.Scatter(x=df_ohlcv.index, y=macd_d["macd"], name="MACD Line", line=dict(color="#29b6f6")), row=3, col=1)
                fig.add_trace(go.Scatter(x=df_ohlcv.index, y=macd_d["signal"], name="Signal Line", line=dict(color="#ff7043")), row=3, col=1)

                fig.update_layout(template="plotly_dark", height=750, xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Error fetching data for {symbol}: {e}")


# ==========================================
# MODULE 2: INDIAN MUTUAL FUND ANALYSIS
# ==========================================
elif mode == "🏦 Mutual Fund Analysis":
    st.markdown(
        '<div class="main-header">🏦 Indian Mutual Fund Analysis (AMFI Data)</div>',
        unsafe_allow_html=True,
    )

    mf_search_query = st.text_input(
        "Search Mutual Fund Scheme by Keyword (e.g. Parag Parikh, SBI Small Cap, Axis Bluechip):",
        value="Parag Parikh Flexi Cap",
    )

    if mf_search_query:
        with st.spinner("Searching AMFI Mutual Fund directory..."):
            results = search_mutual_fund(mf_search_query)

        if results:
            scheme_options = {f"{r['schemeName']} (Code: {r['schemeCode']})": r["schemeCode"] for r in results[:10]}
            selected_option = st.selectbox("Select Scheme Code:", list(scheme_options.keys()))
            selected_code = scheme_options[selected_option]

            with st.spinner(f"Analyzing NAV history for Scheme Code {selected_code}..."):
                details = get_mutual_fund_details(selected_code)
                nav_df = get_mutual_fund_nav_df(selected_code)
                mf_analysis = analyze_mutual_fund_performance(nav_df)

                # Key Metrics Header
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Latest NAV", f"₹{mf_analysis.get('latestNav', 0):,.2f}", f"As of {details.get('latestDate')}")
                m2.metric("CAGR Since Inception", f"{mf_analysis.get('cagrInception', 0)}%")
                m3.metric("Sharpe Ratio", f"{mf_analysis.get('sharpeRatio', 0)}")
                m4.metric("Max Drawdown", f"-{mf_analysis.get('maxDrawdown', {}).get('maxDrawdownPercent', 0)}%")

                st.markdown("---")

                # Details Table & Rolling Returns
                col_det, col_roll = st.columns(2)
                with col_det:
                    st.subheader("📋 Scheme Metadata & CAGRs")
                    st.markdown(f"**Fund House**: {details.get('fundHouse')}")
                    st.markdown(f"**Category**: {details.get('schemeCategory')}")
                    st.markdown(f"**History Analyzed**: {mf_analysis.get('totalYearsHistory')} Years")
                    st.markdown(f"**1-Year CAGR**: `{mf_analysis.get('cagr1Y')}%`")
                    st.markdown(f"**3-Year CAGR**: `{mf_analysis.get('cagr3Y')}%`")
                    st.markdown(f"**5-Year CAGR**: `{mf_analysis.get('cagr5Y')}%`")

                with col_roll:
                    st.subheader("📉 Risk & Rolling Returns")
                    st.markdown(f"**Annualized Volatility**: `{mf_analysis.get('annualizedVolatility')}%`")
                    st.markdown(f"**Sortino Ratio**: `{mf_analysis.get('sortinoRatio')}`")
                    
                    roll = mf_analysis.get("rollingReturns1Y", {})
                    st.markdown(f"**1-Year Rolling Returns (Avg)**: `{roll.get('averageRollingReturn')}%`")
                    st.markdown(f"**1-Year Rolling Returns (Min)**: `{roll.get('minRollingReturn')}%`")
                    st.markdown(f"**1-Year Rolling Returns (Max)**: `{roll.get('maxRollingReturn')}%`")
                    st.markdown(f"**Positive Return Years**: `{roll.get('positivePercentage')}%`")

                st.markdown("---")

                # Plotly NAV Growth Curve
                st.subheader("📊 Interactive NAV Growth Curve & Underwater Drawdown")
                nav_series = nav_df["nav"]
                cummax = nav_series.cummax()
                drawdown_pct = ((nav_series - cummax) / cummax) * 100.0

                fig_mf = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3])
                fig_mf.add_trace(go.Scatter(x=nav_df.index, y=nav_series, name="NAV (₹)", line=dict(color="#00e676")), row=1, col=1)
                fig_mf.add_trace(go.Scatter(x=nav_df.index, y=drawdown_pct, name="Drawdown (%)", line=dict(color="#ff5252"), fill="tozeroy"), row=2, col=1)
                fig_mf.update_layout(template="plotly_dark", height=650)
                st.plotly_chart(fig_mf, use_container_width=True)

        else:
            st.warning("No matching mutual fund scheme found.")


# ==========================================
# MODULE 3: MULTI-ASSET COMPARISON
# ==========================================
elif mode == "⚡ Multi-Asset Comparison":
    st.markdown(
        '<div class="main-header">⚡ Multi-Asset Comparison (vs NIFTY 50 Benchmark)</div>',
        unsafe_allow_html=True,
    )

    comp_type = st.radio("Select Comparison Category:", ["Stocks vs Stocks", "Mutual Funds vs Mutual Funds"], horizontal=True)
    comp_period = st.selectbox("Select Duration:", ["3mo", "6mo", "1y", "3y", "5y"], index=2)

    if comp_type == "Stocks vs Stocks":
        stock_list_input = st.text_input(
            "Enter Stock Tickers (comma separated):",
            value="RELIANCE, TCS, HDFCBANK, INFY",
        )
        if stock_list_input:
            tickers = [t.strip() for t in stock_list_input.split(",") if t.strip()]
            with st.spinner("Generating Stock Comparison Chart..."):
                fig_comp = go.Figure()
                
                # Benchmark NIFTY 50
                nifty_df = get_historical_ohlcv("^NSEI", period=comp_period)
                if not nifty_df.empty and len(nifty_df) > 1:
                    nifty_norm = ((nifty_df["Close"] / nifty_df["Close"].iloc[0]) - 1.0) * 100.0
                    fig_comp.add_trace(go.Scatter(x=nifty_df.index, y=nifty_norm, name=f"NIFTY 50 ({nifty_norm.iloc[-1]:+.1f}%)", line=dict(color="#ffffff", dash="dash", width=2.5)))

                colors = ["#29b6f6", "#ab47bc", "#ffa726", "#26a69a", "#ff7043"]
                for i, tk in enumerate(tickers):
                    sym = normalize_indian_symbol(tk)
                    df = get_historical_ohlcv(sym, period=comp_period)
                    if not df.empty and len(df) > 1:
                        series = df["Close"]
                        norm = ((series / series.iloc[0]) - 1.0) * 100.0
                        fig_comp.add_trace(go.Scatter(x=df.index, y=norm, name=f"{sym} ({norm.iloc[-1]:+.1f}%)", line=dict(color=colors[i % len(colors)], width=2)))

                fig_comp.update_layout(template="plotly_dark", height=600, yaxis_title="Percentage Return (%)", hovermode="x unified")
                st.plotly_chart(fig_comp, use_container_width=True)

    else:
        st.info("Searching Mutual Funds for Comparison...")
        mf1 = st.text_input("Mutual Fund 1 (e.g. Parag Parikh Flexi Cap):", value="Parag Parikh Flexi Cap")
        mf2 = st.text_input("Mutual Fund 2 (e.g. SBI Small Cap):", value="SBI Small Cap")

        if mf1 and mf2:
            res1 = search_mutual_fund(mf1)
            res2 = search_mutual_fund(mf2)

            if res1 and res2:
                c1 = res1[0]["schemeCode"]
                c2 = res2[0]["schemeCode"]
                n1 = res1[0]["schemeName"][:25]
                n2 = res2[0]["schemeName"][:25]

                with st.spinner("Generating Mutual Fund Comparison Chart..."):
                    fig_mf_comp = go.Figure()

                    # Nifty Benchmark
                    nifty_df = get_historical_ohlcv("^NSEI", period=comp_period)
                    if not nifty_df.empty and len(nifty_df) > 1:
                        nifty_norm = ((nifty_df["Close"] / nifty_df["Close"].iloc[0]) - 1.0) * 100.0
                        fig_mf_comp.add_trace(go.Scatter(x=nifty_df.index, y=nifty_norm, name=f"NIFTY 50 ({nifty_norm.iloc[-1]:+.1f}%)", line=dict(color="#ffffff", dash="dash", width=2.5)))

                    days_map = {"3mo": 90, "6mo": 180, "1y": 365, "3y": 1095, "5y": 1825}
                    days = days_map.get(comp_period, 365)

                    for code, name, color in [(c1, n1, "#00e676"), (c2, n2, "#ffb300")]:
                        df_mf = get_mutual_fund_nav_df(code)
                        if not df_mf.empty:
                            start_date = df_mf.index.max() - pd.Timedelta(days=days)
                            sub = df_mf.loc[df_mf.index >= start_date]
                            if len(sub) > 1:
                                norm_mf = ((sub["nav"] / sub["nav"].iloc[0]) - 1.0) * 100.0
                                fig_mf_comp.add_trace(go.Scatter(x=sub.index, y=norm_mf, name=f"{name} ({norm_mf.iloc[-1]:+.1f}%)", line=dict(color=color, width=2)))

                    fig_mf_comp.update_layout(template="plotly_dark", height=600, yaxis_title="Percentage Return (%)", hovermode="x unified")
                    st.plotly_chart(fig_mf_comp, use_container_width=True)


# ==========================================
# MODULE 4: STOCK PEER COMPARISON MATRIX
# ==========================================
elif mode == "🏢 Stock Peer Comparison Matrix":
    st.markdown(
        '<div class="main-header">🏢 Stock Peer Fundamental Comparison Matrix</div>',
        unsafe_allow_html=True,
    )

    peer_input = st.text_input(
        "Enter Stock Tickers to Compare (comma separated e.g. TCS, INFY, WIPRO, HCLTECH):",
        value="TCS, INFY, WIPRO, HCLTECH",
    )

    if peer_input:
        tickers = [t.strip() for t in peer_input.split(",") if t.strip()]
        with st.spinner(f"Computing fundamental scorecard matrix for {len(tickers)} peer companies..."):
            matrix_data = []
            scores = []
            symbols = []

            for tk in tickers:
                sym = normalize_indian_symbol(tk)
                try:
                    quote = get_stock_quote(sym)
                    fund = get_stock_fundamentals(sym)
                    scorecard = compute_financial_health_scorecard(fund)
                    
                    df_ohlcv = get_historical_ohlcv(sym, period="6mo")
                    ta = get_full_technical_analysis(df_ohlcv)

                    score = scorecard.get("healthScore", 0)
                    scores.append(score)
                    symbols.append(sym)

                    matrix_data.append({
                        "Ticker": sym,
                        "Company Name": fund.get("companyName", sym),
                        "Price (₹)": f"₹{quote.get('currentPrice', 0):,.2f}",
                        "Market Cap (Cr)": f"₹{(quote.get('marketCap', 0) or 0) / 10**7:,.0f} Cr",
                        "Health Score": f"{score} / 100",
                        "Valuation Status": scorecard.get("valuationStatus", "N/A"),
                        "Trailing P/E": f"{fund.get('trailingPE', 0):.2f}" if fund.get('trailingPE') else "N/A",
                        "Forward P/E": f"{fund.get('forwardPE', 0):.2f}" if fund.get('forwardPE') else "N/A",
                        "Price / Book": f"{fund.get('priceToBook', 0):.2f}" if fund.get('priceToBook') else "N/A",
                        "EV / EBITDA": f"{fund.get('enterpriseToEbitda', 0):.2f}" if fund.get('enterpriseToEbitda') else "N/A",
                        "Technical Sentiment": ta.get("overallSentiment", "NEUTRAL"),
                    })
                except Exception as e:
                    st.warning(f"Could not process peer symbol {sym}: {e}")

            if matrix_data:
                df_matrix = pd.DataFrame(matrix_data)
                st.subheader("📋 Peer Fundamental Scorecard Matrix")
                st.dataframe(df_matrix, use_container_width=True)

                st.markdown("---")

                # Plotly Comparison Bar Charts
                col_b1, col_b2 = st.columns(2)

                with col_b1:
                    st.subheader("🧮 Health Score Comparison (0 - 100)")
                    fig_score = go.Figure(go.Bar(
                        x=symbols,
                        y=scores,
                        marker_color=["#00e676" if s >= 70 else "#ffa726" if s >= 50 else "#ef5350" for s in scores],
                        text=[f"{s}/100" for s in scores],
                        textposition="auto",
                    ))
                    fig_score.update_layout(template="plotly_dark", height=400, yaxis=dict(range=[0, 100]))
                    st.plotly_chart(fig_score, use_container_width=True)

                with col_b2:
                    st.subheader("📊 Trailing P/E Ratio Comparison")
                    pes = [float(row["Trailing P/E"]) if row["Trailing P/E"] != "N/A" else 0 for row in matrix_data]
                    fig_pe = go.Figure(go.Bar(
                        x=symbols,
                        y=pes,
                        marker_color="#29b6f6",
                        text=[f"{p:.1f}" if p > 0 else "N/A" for p in pes],
                        textposition="auto",
                    ))
                    fig_pe.update_layout(template="plotly_dark", height=400, yaxis_title="P/E Ratio")
                    st.plotly_chart(fig_pe, use_container_width=True)


# ==========================================
# MODULE 5: AI FINANCIAL AGENT
# ==========================================
elif mode == "🤖 AI Financial Agent":
    st.markdown(
        '<div class="main-header">🤖 AI Financial Analyst Assistant</div>',
        unsafe_allow_html=True,
    )

    st.markdown("Ask Arthra Financial Analyst agent any question in natural language:")
    agent_query = st.text_input(
        "Enter query:",
        value="Analyze Reliance Industries stock technically and fundamentally",
    )

    if st.button("🚀 Run Agent Analysis"):
        with st.spinner("Executing MCP tools and synthesizing financial research report..."):
            try:
                agent = FinancialAnalystAgent()
                res = agent.process_natural_language_query(agent_query)

                st.success(f"Report generated! Saved to `{res.get('reportPath')}`")
                st.markdown("---")
                st.markdown(res.get("reportMarkdown"))

            except Exception as e:
                st.error(f"Error executing agent query: {e}")
