"""
Plotly Visualization Engine for Arthra MCP.
Generates interactive Candlestick technical charts, Mutual Fund NAV trajectory & drawdown plots,
and separate Stock & Mutual Fund Comparison charts saved to interactive HTML files.
"""

from typing import Dict, Any, List, Optional
import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging

from src.data.stock_fetcher import get_historical_ohlcv, normalize_indian_symbol
from src.data.mf_fetcher import get_mutual_fund_nav_df, get_mutual_fund_details
from src.analytics.technicals import (
    calculate_sma,
    calculate_ema,
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CHARTS_DIR = os.path.abspath("charts")
os.makedirs(CHARTS_DIR, exist_ok=True)


def build_stock_technical_chart(
    symbol: str, period: str = "1y", save_filename: Optional[str] = None
) -> str:
    """
    Builds a 3-panel interactive Plotly technical chart for an Indian stock:
      - Panel 1: Candlesticks + SMA 20/50/200 & EMA 9/21 + Volume
      - Panel 2: RSI (14) with 70/30 threshold lines
      - Panel 3: MACD Line, Signal Line & Histogram

    Returns:
        Absolute filepath to the saved interactive HTML chart.
    """
    ticker_symbol = normalize_indian_symbol(symbol)
    # Fetch 2y history for indicator warmup so RSI and 200 SMA span 100% of visible chart
    warmup_period = "2y" if period in ["1mo", "3mo", "6mo", "1y"] else "5y"
    full_df = get_historical_ohlcv(ticker_symbol, period=warmup_period)
    
    if full_df.empty or len(full_df) < 20:
        raise ValueError(f"Insufficient OHLCV price data for {ticker_symbol}")

    # Compute Indicators on full warmup DataFrame
    full_df["SMA_20"] = calculate_sma(full_df, 20)
    full_df["SMA_50"] = calculate_sma(full_df, 50)
    full_df["SMA_200"] = calculate_sma(full_df, 200)
    full_df["EMA_9"] = calculate_ema(full_df, 9)
    full_df["EMA_21"] = calculate_ema(full_df, 21)
    
    full_df["RSI"] = calculate_rsi(full_df, 14)
    macd_dict = calculate_macd(full_df)
    full_df["MACD"] = macd_dict["macd"]
    full_df["MACD_Signal"] = macd_dict["signal"]
    full_df["MACD_Hist"] = macd_dict["histogram"]
    
    bb_dict = calculate_bollinger_bands(full_df)
    full_df["BB_Upper"] = bb_dict["upper"]
    full_df["BB_Lower"] = bb_dict["lower"]

    # Crop to requested display period date range
    period_map = {"1mo": 30, "3mo": 90, "6mo": 180, "1y": 365, "2y": 730, "3y": 1095}
    display_days = period_map.get(period.lower(), 365)
    start_display = full_df.index.max() - pd.Timedelta(days=display_days)
    df = full_df.loc[full_df.index >= start_display].copy()

    sma20 = df["SMA_20"]
    sma50 = df["SMA_50"]
    sma200 = df["SMA_200"]
    ema9 = df["EMA_9"]
    ema21 = df["EMA_21"]
    rsi = df["RSI"]
    macd_line = df["MACD"]
    macd_signal = df["MACD_Signal"]
    macd_hist = df["MACD_Hist"]
    bb_upper = df["BB_Upper"]
    bb_lower = df["BB_Lower"]

    # Subplot Layout: 3 Rows
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.60, 0.20, 0.20],
        subplot_titles=(
            f"<b>{ticker_symbol}</b> — Price & Moving Averages",
            "<b>RSI (14)</b> Relative Strength Index",
            "<b>MACD</b> Moving Average Convergence Divergence"
        )
    )

    # 1. Candlestick Chart (Row 1)
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="OHLC Price",
            increasing_line_color="#26a69a",
            decreasing_line_color="#ef5350"
        ),
        row=1, col=1
    )

    # Overlays (MAs)
    fig.add_trace(go.Scatter(x=df.index, y=sma20, mode="lines", name="SMA 20", line=dict(color="#29b6f6", width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=sma50, mode="lines", name="SMA 50", line=dict(color="#ab47bc", width=1.5)), row=1, col=1)
    if sma200 is not None:
        fig.add_trace(go.Scatter(x=df.index, y=sma200, mode="lines", name="SMA 200", line=dict(color="#ffa726", width=2.0)), row=1, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=ema9, mode="lines", name="EMA 9", line=dict(color="#26c6da", width=1, dash="dot")), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=ema21, mode="lines", name="EMA 21", line=dict(color="#ff7043", width=1, dash="dot")), row=1, col=1)

    # Bollinger Bands
    fig.add_trace(go.Scatter(x=df.index, y=bb_upper, mode="lines", name="BB Upper", line=dict(color="rgba(180, 180, 180, 0.4)", width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=bb_lower, mode="lines", name="BB Lower", line=dict(color="rgba(180, 180, 180, 0.4)", width=1), fill="tonexty", fillcolor="rgba(180, 180, 180, 0.05)"), row=1, col=1)

    # 2. RSI Subplot (Row 2)
    fig.add_trace(
        go.Scatter(x=df.index, y=rsi, mode="lines", name="RSI 14", line=dict(color="#ab47bc", width=1.8)),
        row=2, col=1
    )
    fig.add_hline(y=70, line_dash="dash", line_color="#ef5350", annotation_text="Overbought (70)", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="#26a69a", annotation_text="Oversold (30)", row=2, col=1)

    # 3. MACD Subplot (Row 3)
    fig.add_trace(go.Scatter(x=df.index, y=macd_line, mode="lines", name="MACD Line", line=dict(color="#29b6f6", width=1.5)), row=3, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=macd_signal, mode="lines", name="Signal Line", line=dict(color="#ff7043", width=1.5)), row=3, col=1)
    
    colors = ["#26a69a" if val >= 0 else "#ef5350" for val in macd_hist]
    fig.add_trace(go.Bar(x=df.index, y=macd_hist, name="Histogram", marker_color=colors), row=3, col=1)

    clean_sym = ticker_symbol.replace(".", "_")
    output_filename = save_filename or f"{clean_sym}_technical.html"
    filepath = os.path.join(CHARTS_DIR, output_filename)

    fig.update_layout(
        template="plotly_dark",
        title=f"<b>Arthra MCP — Technical Analysis Chart: {ticker_symbol}</b>",
        xaxis_rangeslider_visible=False,
        height=850,
        margin=dict(l=50, r=40, t=70, b=50),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.write_html(filepath)
    logger.info(f"Saved interactive technical chart to: {filepath}")
    return filepath


def build_mutual_fund_chart(
    scheme_code: str | int, save_filename: Optional[str] = None
) -> str:
    """
    Builds a 2-panel interactive Plotly chart for an Indian Mutual Fund:
      - Panel 1: NAV Growth Trajectory Curve
      - Panel 2: Underwater Drawdown (%)

    Returns:
        Absolute filepath to the saved interactive HTML chart.
    """
    details = get_mutual_fund_details(scheme_code)
    scheme_name = details.get("schemeName", f"Scheme {scheme_code}")
    nav_df = get_mutual_fund_nav_df(scheme_code)

    if nav_df.empty:
        raise ValueError(f"No NAV data available for scheme code {scheme_code}")

    nav_series = nav_df["nav"]
    cummax = nav_series.cummax()
    drawdown_pct = ((nav_series - cummax) / cummax) * 100.0

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights=[0.70, 0.30],
        subplot_titles=(
            f"<b>{scheme_name}</b> — NAV Growth Trajectory",
            "<b>Underwater Drawdown (%)</b> Peak-to-Trough Decline"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=nav_df.index,
            y=nav_series,
            mode="lines",
            name="NAV (₹)",
            line=dict(color="#00e676", width=2.2),
            fill="tozeroy",
            fillcolor="rgba(0, 230, 118, 0.05)"
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=nav_df.index,
            y=drawdown_pct,
            mode="lines",
            name="Drawdown (%)",
            line=dict(color="#ff5252", width=1.5),
            fill="tozeroy",
            fillcolor="rgba(255, 82, 82, 0.2)"
        ),
        row=2, col=1
    )

    output_filename = save_filename or f"MF_{scheme_code}_performance.html"
    filepath = os.path.join(CHARTS_DIR, output_filename)

    fig.update_layout(
        template="plotly_dark",
        title=f"<b>Arthra MCP — Mutual Fund Performance: {scheme_name}</b>",
        height=700,
        margin=dict(l=50, r=40, t=70, b=50),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.write_html(filepath)
    logger.info(f"Saved interactive Mutual Fund chart to: {filepath}")
    return filepath


def build_stock_comparison_chart(
    stocks_dict: Dict[str, str], period: str = "1y", save_filename: Optional[str] = None
) -> str:
    """
    Compares performance of multiple Indian Stocks normalized on a 0% baseline vs NIFTY 50 benchmark.
    
    Args:
        stocks_dict: Dict mapping Stock Label to Symbol (e.g. {'Reliance': 'RELIANCE', 'TCS': 'TCS.NS'})
        period: Time period ('1mo', '3mo', '6mo', '1y', '3y', '5y')
    """
    fig = go.Figure()
    
    # Benchmark: NIFTY 50
    nifty_df = get_historical_ohlcv("^NSEI", period=period)
    if not nifty_df.empty and len(nifty_df) > 1:
        nifty_norm = ((nifty_df["Close"] / nifty_df["Close"].iloc[0]) - 1.0) * 100.0
        fig.add_trace(
            go.Scatter(
                x=nifty_df.index,
                y=nifty_norm,
                mode="lines",
                name=f"NIFTY 50 Benchmark ({nifty_norm.iloc[-1]:+.1f}%)",
                line=dict(color="#ffffff", width=2.5, dash="dash")
            )
        )

    colors = ["#29b6f6", "#ab47bc", "#ffa726", "#26a69a", "#ff7043", "#ec407a"]
    color_idx = 0

    for label, symbol in stocks_dict.items():
        try:
            df = get_historical_ohlcv(symbol, period=period)
            if not df.empty and "Close" in df.columns and len(df) > 1:
                series = df["Close"]
                norm_series = ((series / series.iloc[0]) - 1.0) * 100.0
                curr_color = colors[color_idx % len(colors)]
                color_idx += 1
                
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=norm_series,
                        mode="lines",
                        name=f"{label} ({norm_series.iloc[-1]:+.1f}%)",
                        line=dict(color=curr_color, width=2.0)
                    )
                )
        except Exception as e:
            logger.warning(f"Error loading stock {label} ({symbol}) for comparison: {e}")

    output_filename = save_filename or "stock_comparison.html"
    filepath = os.path.join(CHARTS_DIR, output_filename)

    fig.update_layout(
        template="plotly_dark",
        title=f"<b>Arthra MCP — Indian Equities Comparison vs NIFTY 50 ({period.upper()})</b>",
        yaxis_title="Percentage Return (%)",
        height=600,
        margin=dict(l=50, r=40, t=70, b=50),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.write_html(filepath)
    logger.info(f"Saved interactive stock comparison chart to: {filepath}")
    return filepath


def build_mutual_fund_comparison_chart(
    mf_dict: Dict[str, str | int], period: str = "1y", save_filename: Optional[str] = None
) -> str:
    """
    Compares performance of multiple Indian Mutual Funds normalized on a 0% baseline vs NIFTY 50 benchmark.
    
    Args:
        mf_dict: Dict mapping Fund Label to Scheme Code (e.g. {'PPFC Fund': '122640', 'SBI Small Cap': 125497})
        period: Time period ('1mo', '3mo', '6mo', '1y', '3y', '5y')
    """
    fig = go.Figure()

    # Benchmark: NIFTY 50
    nifty_df = get_historical_ohlcv("^NSEI", period=period)
    if not nifty_df.empty and len(nifty_df) > 1:
        nifty_norm = ((nifty_df["Close"] / nifty_df["Close"].iloc[0]) - 1.0) * 100.0
        fig.add_trace(
            go.Scatter(
                x=nifty_df.index,
                y=nifty_norm,
                mode="lines",
                name=f"NIFTY 50 Benchmark ({nifty_norm.iloc[-1]:+.1f}%)",
                line=dict(color="#ffffff", width=2.5, dash="dash")
            )
        )

    period_map = {"1mo": 30, "3mo": 90, "6mo": 180, "1y": 365, "2y": 730, "3y": 1095, "5y": 1825}
    days = period_map.get(period.lower(), 365)

    colors = ["#00e676", "#29b6f6", "#ffb300", "#ff4081", "#7c4dff", "#1de9b6"]
    color_idx = 0

    for label, scheme_code in mf_dict.items():
        try:
            df = get_mutual_fund_nav_df(scheme_code)
            if not df.empty and "nav" in df.columns:
                # Filter to requested period
                start_date = df.index.max() - pd.Timedelta(days=days)
                sub_df = df.loc[df.index >= start_date].copy()
                
                if len(sub_df) > 1:
                    series = sub_df["nav"]
                    norm_series = ((series / series.iloc[0]) - 1.0) * 100.0
                    curr_color = colors[color_idx % len(colors)]
                    color_idx += 1
                    
                    fig.add_trace(
                        go.Scatter(
                            x=sub_df.index,
                            y=norm_series,
                            mode="lines",
                            name=f"{label} ({norm_series.iloc[-1]:+.1f}%)",
                            line=dict(color=curr_color, width=2.0)
                        )
                    )
        except Exception as e:
            logger.warning(f"Error loading mutual fund {label} ({scheme_code}) for comparison: {e}")

    output_filename = save_filename or "mf_comparison.html"
    filepath = os.path.join(CHARTS_DIR, output_filename)

    fig.update_layout(
        template="plotly_dark",
        title=f"<b>Arthra MCP — Indian Mutual Funds Comparison vs NIFTY 50 ({period.upper()})</b>",
        yaxis_title="Percentage Return (%)",
        height=600,
        margin=dict(l=50, r=40, t=70, b=50),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig.write_html(filepath)
    logger.info(f"Saved interactive mutual fund comparison chart to: {filepath}")
    return filepath


def build_benchmark_comparison_chart(
    assets_dict: Dict[str, str], period: str = "1y", save_filename: Optional[str] = None
) -> str:
    """General asset comparison helper."""
    # Split into stocks vs MFs
    stocks = {k: v for k, v in assets_dict.items() if not str(v).isdigit()}
    mfs = {k: v for k, v in assets_dict.items() if str(v).isdigit()}

    if stocks and not mfs:
        return build_stock_comparison_chart(stocks, period=period, save_filename=save_filename)
    elif mfs and not stocks:
        return build_mutual_fund_comparison_chart(mfs, period=period, save_filename=save_filename)
    else:
        # Default to stock comparison if mixed
        return build_stock_comparison_chart(stocks, period=period, save_filename=save_filename)
