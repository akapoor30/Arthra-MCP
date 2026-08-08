"""
Technical Analysis & Quantitative Metrics Engine for Stocks.
Calculates Moving Averages (SMA/EMA), RSI, MACD, Bollinger Bands, Beta vs NIFTY 50, and Technical Crossover Signals.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
import logging
from src.data.stock_fetcher import get_historical_ohlcv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default RBI / Indian Risk-Free Rate ~6.5%
RISK_FREE_RATE_ANNUAL = 0.065


def calculate_sma(df: pd.DataFrame, window: int = 20, column: str = "Close") -> pd.Series:
    """Calculates Simple Moving Average (SMA)."""
    return df[column].rolling(window=window).mean()


def calculate_ema(df: pd.DataFrame, span: int = 20, column: str = "Close") -> pd.Series:
    """Calculates Exponential Moving Average (EMA)."""
    return df[column].ewm(span=span, adjust=False).mean()


def calculate_rsi(df: pd.DataFrame, window: int = 14, column: str = "Close") -> pd.Series:
    """
    Calculates Relative Strength Index (RSI) using Wilder's exponential smoothing.
    """
    delta = df[column].diff()
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)
    
    # Exponential Weighted Moving Average (Wilder smoothing)
    avg_gain = gain.ewm(alpha=1/window, min_periods=window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/window, min_periods=window, adjust=False).mean()
    
    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(
    df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9, column: str = "Close"
) -> Dict[str, pd.Series]:
    """
    Calculates Moving Average Convergence Divergence (MACD).
    Returns dict with keys: 'macd', 'signal', 'histogram'.
    """
    ema_fast = df[column].ewm(span=fast, adjust=False).mean()
    ema_slow = df[column].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    
    return {
        "macd": macd_line,
        "signal": signal_line,
        "histogram": histogram
    }


def calculate_bollinger_bands(
    df: pd.DataFrame, window: int = 20, num_std: float = 2.0, column: str = "Close"
) -> Dict[str, pd.Series]:
    """
    Calculates Bollinger Bands (Middle, Upper, Lower, Bandwidth %).
    """
    sma = df[column].rolling(window=window).mean()
    std = df[column].rolling(window=window).std()
    upper = sma + (num_std * std)
    lower = sma - (num_std * std)
    bandwidth = ((upper - lower) / sma) * 100
    
    return {
        "middle": sma,
        "upper": upper,
        "lower": lower,
        "bandwidth": bandwidth
    }


def calculate_beta_and_volatility(
    stock_df: pd.DataFrame, benchmark_symbol: str = "^NSEI", period: str = "1y"
) -> Dict[str, float]:
    """
    Computes annualized volatility and Beta relative to benchmark (default: NIFTY 50 '^NSEI').
    """
    try:
        benchmark_df = get_historical_ohlcv(benchmark_symbol, period=period, interval="1d")
        if benchmark_df.empty or "Close" not in benchmark_df.columns:
            return {"volatility": 0.0, "beta": 1.0}
            
        stock_returns = stock_df["Close"].pct_change().dropna()
        bench_returns = benchmark_df["Close"].pct_change().dropna()
        
        # Align dates
        aligned = pd.concat([stock_returns, bench_returns], axis=1, join="inner").dropna()
        aligned.columns = ["stock", "benchmark"]
        
        if len(aligned) < 20:
            return {"volatility": 0.0, "beta": 1.0}
            
        cov_matrix = np.cov(aligned["stock"], aligned["benchmark"])
        covariance = cov_matrix[0, 1]
        bench_variance = cov_matrix[1, 1]
        
        beta = covariance / (bench_variance + 1e-10)
        ann_volatility = aligned["stock"].std() * np.sqrt(252)
        
        return {
            "volatility": round(float(ann_volatility * 100), 2),  # Percentage
            "beta": round(float(beta), 2)
        }
    except Exception as e:
        logger.warning(f"Error calculating beta/volatility: {e}")
        return {"volatility": 0.0, "beta": 1.0}


def get_full_technical_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Runs full quantitative technical analysis pipeline on stock OHLCV DataFrame.
    Returns calculated indicator values, latest candle metrics, and signal summary.
    """
    if df.empty or len(df) < 20:
        return {"error": "Insufficient OHLCV history for technical analysis"}
        
    df_ta = df.copy()
    
    # Calculate MAs
    df_ta["SMA_20"] = calculate_sma(df_ta, 20)
    df_ta["SMA_50"] = calculate_sma(df_ta, 50)
    df_ta["SMA_200"] = calculate_sma(df_ta, 200) if len(df_ta) >= 200 else np.nan
    df_ta["EMA_9"] = calculate_ema(df_ta, 9)
    df_ta["EMA_21"] = calculate_ema(df_ta, 21)
    
    # Calculate Oscillators & Bands
    df_ta["RSI"] = calculate_rsi(df_ta, 14)
    macd_dict = calculate_macd(df_ta)
    df_ta["MACD"] = macd_dict["macd"]
    df_ta["MACD_Signal"] = macd_dict["signal"]
    df_ta["MACD_Hist"] = macd_dict["histogram"]
    
    bb_dict = calculate_bollinger_bands(df_ta)
    df_ta["BB_Middle"] = bb_dict["middle"]
    df_ta["BB_Upper"] = bb_dict["upper"]
    df_ta["BB_Lower"] = bb_dict["lower"]
    
    # Latest Values
    latest = df_ta.iloc[-1]
    prev = df_ta.iloc[-2] if len(df_ta) > 1 else latest
    
    close_val = float(latest["Close"])
    rsi_val = float(latest["RSI"]) if not pd.isna(latest["RSI"]) else 50.0
    sma20_val = float(latest["SMA_20"]) if not pd.isna(latest["SMA_20"]) else close_val
    sma50_val = float(latest["SMA_50"]) if not pd.isna(latest["SMA_50"]) else close_val
    sma200_val = float(latest["SMA_200"]) if not pd.isna(latest["SMA_200"]) else None
    
    macd_val = float(latest["MACD"]) if not pd.isna(latest["MACD"]) else 0.0
    macd_signal_val = float(latest["MACD_Signal"]) if not pd.isna(latest["MACD_Signal"]) else 0.0
    macd_hist_val = float(latest["MACD_Hist"]) if not pd.isna(latest["MACD_Hist"]) else 0.0
    
    # Signal Logic Assessment
    signals = []
    bullish_points = 0
    bearish_points = 0
    
    # MA Crossovers & Trend
    if close_val > sma20_val:
        signals.append("Price above 20 SMA (Short-term uptrend)")
        bullish_points += 1
    else:
        signals.append("Price below 20 SMA (Short-term weakness)")
        bearish_points += 1
        
    if close_val > sma50_val:
        signals.append("Price above 50 SMA (Medium-term uptrend)")
        bullish_points += 1
    else:
        signals.append("Price below 50 SMA (Medium-term weakness)")
        bearish_points += 1
        
    if sma200_val is not None:
        if close_val > sma200_val:
            signals.append("Price above 200 SMA (Long-term Bullish regime)")
            bullish_points += 2
        else:
            signals.append("Price below 200 SMA (Long-term Bearish regime)")
            bearish_points += 2
            
    # RSI Signals
    if rsi_val > 70:
        signals.append(f"RSI Overbought ({rsi_val:.1f}) — Caution for potential pullbacks")
        bearish_points += 1
    elif rsi_val < 30:
        signals.append(f"RSI Oversold ({rsi_val:.1f}) — Potential reversal / rebound zone")
        bullish_points += 1
    else:
        signals.append(f"RSI Neutral ({rsi_val:.1f})")
        
    # MACD Crossovers
    if macd_val > macd_signal_val:
        signals.append("MACD Line above Signal Line (Bullish Momentum)")
        bullish_points += 1
    else:
        signals.append("MACD Line below Signal Line (Bearish Momentum)")
        bearish_points += 1
        
    # Overall Sentiment
    if bullish_points >= bearish_points + 2:
        sentiment = "STRONG BULLISH"
    elif bullish_points > bearish_points:
        sentiment = "BULLISH"
    elif bearish_points >= bullish_points + 2:
        sentiment = "STRONG BEARISH"
    elif bearish_points > bullish_points:
        sentiment = "BEARISH"
    else:
        sentiment = "NEUTRAL"

    return {
        "latestClose": round(close_val, 2),
        "rsi": round(rsi_val, 2),
        "sma20": round(sma20_val, 2),
        "sma50": round(sma50_val, 2),
        "sma200": round(sma200_val, 2) if sma200_val else "N/A",
        "ema9": round(float(latest["EMA_9"]), 2),
        "ema21": round(float(latest["EMA_21"]), 2),
        "macd": round(macd_val, 2),
        "macdSignal": round(macd_signal_val, 2),
        "macdHist": round(macd_hist_val, 2),
        "bbUpper": round(float(latest["BB_Upper"]), 2),
        "bbMiddle": round(float(latest["BB_Middle"]), 2),
        "bbLower": round(float(latest["BB_Lower"]), 2),
        "overallSentiment": sentiment,
        "signalHighlights": signals,
        "processedDataFrame": df_ta
    }
