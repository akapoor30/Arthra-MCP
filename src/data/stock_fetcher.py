"""
Stock Data Fetcher Module for Indian Equities (NSE/BSE).
Ingests market quotes, historical OHLCV candles, valuation ratios, and financial statements via yfinance.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import yfinance as yf
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def normalize_indian_symbol(symbol: str) -> str:
    """
    Normalizes stock ticker symbol to NSE/BSE format.
    Defaults to NSE (.NS) if no exchange suffix (.NS or .BO) is provided.
    Preserves index tickers starting with '^' (e.g., '^NSEI', '^BSESN').
    """
    cleaned = symbol.strip().upper()
    if cleaned.startswith("^"):
        return cleaned
    if cleaned.endswith(".NS") or cleaned.endswith(".BO"):
        return cleaned
    # Default to NSE (.NS) for Indian market tickers
    return f"{cleaned}.NS"


def get_stock_quote(symbol: str) -> Dict[str, Any]:
    """
    Fetches real-time price quote and essential market summary for an Indian stock.
    """
    ticker_symbol = normalize_indian_symbol(symbol)
    logger.info(f"Fetching stock quote for: {ticker_symbol}")
    
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    
    if not info or ("regularMarketPrice" not in info and "currentPrice" not in info and "previousClose" not in info):
        # Retry with .BO if .NS returned no data and user supplied no suffix
        if not symbol.upper().endswith(".NS") and not symbol.upper().endswith(".BO"):
            bo_symbol = f"{symbol.strip().upper()}.BO"
            logger.info(f"Retrying quote fetch with BSE symbol: {bo_symbol}")
            ticker = yf.Ticker(bo_symbol)
            info = ticker.info
            ticker_symbol = bo_symbol

    current_price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
    prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose")
    
    change = (current_price - prev_close) if (current_price and prev_close) else 0.0
    p_change = (change / prev_close * 100.0) if (prev_close and prev_close > 0) else 0.0

    return {
        "symbol": ticker_symbol,
        "shortName": info.get("shortName") or info.get("longName") or ticker_symbol,
        "exchange": info.get("exchange", "NSE"),
        "currency": info.get("currency", "INR"),
        "currentPrice": current_price,
        "previousClose": prev_close,
        "open": info.get("open") or info.get("regularMarketOpen"),
        "dayHigh": info.get("dayHigh") or info.get("regularMarketDayHigh"),
        "dayLow": info.get("dayLow") or info.get("regularMarketDayLow"),
        "change": round(change, 2),
        "percentChange": round(p_change, 2),
        "volume": info.get("volume") or info.get("regularMarketVolume"),
        "marketCap": info.get("marketCap"),
        "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
        "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
        "fiftyDayAverage": info.get("fiftyDayAverage"),
        "twoHundredDayAverage": info.get("twoHundredDayAverage"),
    }


def get_historical_ohlcv(
    symbol: str, period: str = "1y", interval: str = "1d"
) -> pd.DataFrame:
    """
    Fetches historical OHLCV data for an Indian stock.
    
    Args:
        symbol: Ticker symbol (e.g. 'RELIANCE', 'TCS.NS')
        period: Data duration ('1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
        interval: Data granularity ('1d', '1wk', '1mo')
        
    Returns:
        pd.DataFrame indexed by Date with columns ['Open', 'High', 'Low', 'Close', 'Volume']
    """
    ticker_symbol = normalize_indian_symbol(symbol)
    logger.info(f"Fetching historical OHLCV ({period}, {interval}) for {ticker_symbol}")
    
    df = yf.download(ticker_symbol, period=period, interval=interval, progress=False)
    
    if df.empty and not symbol.upper().endswith(".NS") and not symbol.upper().endswith(".BO"):
        bo_symbol = f"{symbol.strip().upper()}.BO"
        logger.info(f"Retrying OHLCV download with BSE symbol: {bo_symbol}")
        df = yf.download(bo_symbol, period=period, interval=interval, progress=False)
        ticker_symbol = bo_symbol

    # Clean multi-level columns if returned by newer yfinance versions
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Clean column names
    df = df.loc[:, ~df.columns.duplicated()]
    required_cols = ["Open", "High", "Low", "Close", "Volume"]
    existing_cols = [c for c in required_cols if c in df.columns]
    df = df[existing_cols].copy()
    df.dropna(subset=["Close"], inplace=True)
    
    return df


def get_stock_fundamentals(symbol: str) -> Dict[str, Any]:
    """
    Fetches comprehensive fundamental metrics, valuation ratios, and financial health scores.
    """
    ticker_symbol = normalize_indian_symbol(symbol)
    logger.info(f"Fetching fundamentals for: {ticker_symbol}")
    
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    
    return {
        "symbol": ticker_symbol,
        "companyName": info.get("longName") or info.get("shortName"),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "marketCap": info.get("marketCap"),
        "trailingPE": info.get("trailingPE"),
        "forwardPE": info.get("forwardPE"),
        "priceToBook": info.get("priceToBook"),
        "enterpriseToEbitda": info.get("enterpriseToEbitda"),
        "enterpriseToRevenue": info.get("enterpriseToRevenue"),
        "dividendYield": info.get("dividendYield"),
        "beta": info.get("beta"),
        "trailingEps": info.get("trailingEps"),
        "forwardEps": info.get("forwardEps"),
        "returnOnEquity": info.get("returnOnEquity"),
        "returnOnAssets": info.get("returnOnAssets"),
        "profitMargins": info.get("profitMargins"),
        "operatingMargins": info.get("operatingMargins"),
        "revenueGrowth": info.get("revenueGrowth"),
        "earningsGrowth": info.get("earningsGrowth"),
        "debtToEquity": info.get("debtToEquity"),
        "quickRatio": info.get("quickRatio"),
        "currentRatio": info.get("currentRatio"),
        "freeCashflow": info.get("freeCashflow"),
        "targetMeanPrice": info.get("targetMeanPrice"),
        "recommendationKey": info.get("recommendationKey"),
    }


def get_financial_statements(symbol: str) -> Dict[str, Any]:
    """
    Fetches Income Statement, Balance Sheet, and Cash Flow Statement (Annual & Quarterly).
    """
    ticker_symbol = normalize_indian_symbol(symbol)
    logger.info(f"Fetching financial statements for: {ticker_symbol}")
    
    ticker = yf.Ticker(ticker_symbol)
    
    income_stmt = ticker.financials
    balance_sheet = ticker.balance_sheet
    cash_flow = ticker.cashflow

    def df_to_dict(df: pd.DataFrame) -> Dict[str, Any]:
        if df is None or df.empty:
            return {}
        # Convert Timestamp headers to str
        df_copy = df.copy()
        df_copy.columns = [str(c)[:10] for c in df_copy.columns]
        return df_copy.fillna(0).to_dict()

    return {
        "symbol": ticker_symbol,
        "incomeStatement": df_to_dict(income_stmt),
        "balanceSheet": df_to_dict(balance_sheet),
        "cashFlow": df_to_dict(cash_flow),
    }
