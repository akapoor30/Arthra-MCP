"""
MCP Tools Implementation for Arthra MCP.
Defines functions for symbol resolution, data ingestion, quantitative analytics, and Plotly chart generation.
"""

from typing import Dict, Any, List, Optional
import os
import logging
from src.data.stock_fetcher import (
    normalize_indian_symbol,
    get_stock_quote,
    get_historical_ohlcv,
    get_stock_fundamentals,
    get_financial_statements,
)
from src.data.mf_fetcher import (
    search_mutual_fund,
    get_mutual_fund_details,
    get_mutual_fund_nav_df,
)
from src.analytics.technicals import (
    get_full_technical_analysis,
    calculate_beta_and_volatility,
)
from src.analytics.fundamentals import compute_financial_health_scorecard
from src.analytics.mf_analytics import analyze_mutual_fund_performance
from src.visualization.chart_builder import (
    build_stock_technical_chart,
    build_mutual_fund_chart,
    build_stock_comparison_chart,
    build_mutual_fund_comparison_chart,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def tool_search_indian_symbol(query: str) -> Dict[str, Any]:
    """
    Resolves an Indian stock symbol or searches AMFI Mutual Fund scheme codes.
    
    Args:
        query: Company name or keyword (e.g., 'RELIANCE', 'TCS', 'Parag Parikh')
    """
    logger.info(f"MCP Tool 'search_indian_symbol' called for: '{query}'")
    query_str = query.strip()
    
    # 1. Search Mutual Funds
    mf_results = search_mutual_fund(query_str)
    
    # 2. Resolve Stock Symbol
    stock_symbol = normalize_indian_symbol(query_str)
    try:
        quote = get_stock_quote(stock_symbol)
        valid_stock = quote.get("currentPrice") is not None and quote.get("currentPrice") > 0
    except Exception:
        valid_stock = False
        quote = {}

    return {
        "query": query_str,
        "resolvedStockSymbol": stock_symbol if valid_stock else None,
        "stockQuoteSummary": quote if valid_stock else None,
        "mutualFundMatches": mf_results[:5] if mf_results else []
    }


def tool_fetch_financial_data(
    symbol: str, data_type: str = "stock", period: str = "1y"
) -> Dict[str, Any]:
    """
    Fetches raw financial market data for Indian Stocks or Mutual Funds.
    
    Args:
        symbol: Stock symbol ('RELIANCE') or Mutual Fund scheme code ('122640')
        data_type: 'stock', 'mutual_fund', 'fundamentals', or 'financials'
        period: Time period ('1mo', '3mo', '6mo', '1y', '2y', '5y')
    """
    logger.info(f"MCP Tool 'fetch_financial_data' called for {symbol} ({data_type}, {period})")
    dt = data_type.lower().strip()
    
    if dt == "mutual_fund" or str(symbol).isdigit():
        details = get_mutual_fund_details(symbol)
        nav_df = get_mutual_fund_nav_df(symbol)
        return {
            "assetType": "Mutual Fund",
            "schemeDetails": details,
            "totalRecords": len(nav_df),
            "latestNav": details.get("latestNav"),
            "latestDate": details.get("latestDate")
        }
    elif dt == "fundamentals":
        return get_stock_fundamentals(symbol)
    elif dt == "financials":
        return get_financial_statements(symbol)
    else:  # Stock
        quote = get_stock_quote(symbol)
        df_ohlcv = get_historical_ohlcv(symbol, period=period)
        return {
            "assetType": "Indian Stock",
            "quote": quote,
            "candleCount": len(df_ohlcv),
            "recentCandles": df_ohlcv.tail(5).reset_index().to_dict(orient="records") if not df_ohlcv.empty else []
        }


def tool_analyze_and_visualize(
    symbol: str, asset_type: str = "stock", period: str = "1y", generate_chart: bool = True
) -> Dict[str, Any]:
    """
    Runs quantitative technical/fundamental/MF risk analysis AND generates interactive Plotly HTML chart.
    
    Args:
        symbol: Stock symbol ('TCS') or Mutual Fund scheme code ('122640')
        asset_type: 'stock' or 'mutual_fund'
        period: Time period ('3mo', '6mo', '1y', '2y', '5y')
        generate_chart: Whether to save interactive HTML chart
    """
    logger.info(f"MCP Tool 'analyze_and_visualize' called for {symbol} ({asset_type})")
    is_mf = asset_type.lower() == "mutual_fund" or str(symbol).isdigit()
    
    if is_mf:
        details = get_mutual_fund_details(symbol)
        scheme_code = details.get("schemeCode", symbol)
        scheme_name = details.get("schemeName", f"Scheme {symbol}")
        nav_df = get_mutual_fund_nav_df(scheme_code)
        
        mf_analysis = analyze_mutual_fund_performance(nav_df)
        
        chart_path = None
        if generate_chart and not nav_df.empty:
            chart_path = build_mutual_fund_chart(scheme_code)
            
        return {
            "assetType": "Mutual Fund",
            "schemeCode": scheme_code,
            "schemeName": scheme_name,
            "fundHouse": details.get("fundHouse"),
            "category": details.get("schemeCategory"),
            "quantitativeAnalysis": mf_analysis,
            "chartPath": chart_path,
            "chartUrl": f"file://{chart_path}" if chart_path else None
        }
    else:  # Stock
        norm_sym = normalize_indian_symbol(symbol)
        df_ohlcv = get_historical_ohlcv(norm_sym, period=period)
        
        ta_results = get_full_technical_analysis(df_ohlcv)
        beta_results = calculate_beta_and_volatility(df_ohlcv)
        
        raw_fund = get_stock_fundamentals(norm_sym)
        health_scorecard = compute_financial_health_scorecard(raw_fund)
        
        chart_path = None
        if generate_chart and not df_ohlcv.empty:
            chart_path = build_stock_technical_chart(norm_sym, period=period)
            
        return {
            "assetType": "Indian Stock",
            "symbol": norm_sym,
            "companyName": raw_fund.get("companyName", norm_sym),
            "sector": raw_fund.get("sector"),
            "technicalAnalysis": {
                "sentiment": ta_results.get("overallSentiment"),
                "rsi": ta_results.get("rsi"),
                "sma20": ta_results.get("sma20"),
                "sma50": ta_results.get("sma50"),
                "sma200": ta_results.get("sma200"),
                "macd": ta_results.get("macd"),
                "signalHighlights": ta_results.get("signalHighlights"),
                "volatility": beta_results.get("volatility"),
                "beta": beta_results.get("beta")
            },
            "fundamentalScorecard": health_scorecard,
            "chartPath": chart_path,
            "chartUrl": f"file://{chart_path}" if chart_path else None
        }


def tool_compare_assets(
    assets: List[str], asset_type: str = "stock", period: str = "1y"
) -> Dict[str, Any]:
    """
    Compares performance of multiple Indian stocks or mutual funds vs NIFTY 50 benchmark on a 0% baseline.
    
    Args:
        assets: List of symbols (e.g. ['RELIANCE', 'TCS', 'HDFCBANK']) or Scheme Codes (e.g. ['122640', '125497'])
        asset_type: 'stock' or 'mutual_fund'
        period: Time period ('3mo', '6mo', '1y', '3y', '5y')
    """
    logger.info(f"MCP Tool 'compare_assets' called for {assets} ({asset_type}, {period})")
    is_mf = asset_type.lower() == "mutual_fund" or any(str(a).isdigit() for a in assets)
    
    if is_mf:
        mf_dict = {}
        for a in assets:
            details = get_mutual_fund_details(a)
            name = details.get("schemeName", f"Scheme {a}")
            mf_dict[name[:25]] = str(a)
            
        chart_path = build_mutual_fund_comparison_chart(mf_dict, period=period)
        return {
            "comparisonType": "Mutual Funds vs NIFTY 50",
            "period": period,
            "assetsCompared": list(mf_dict.keys()),
            "chartPath": chart_path,
            "chartUrl": f"file://{chart_path}"
        }
    else:
        stock_dict = {normalize_indian_symbol(a): normalize_indian_symbol(a) for a in assets}
        chart_path = build_stock_comparison_chart(stock_dict, period=period)
        return {
            "comparisonType": "Indian Equities vs NIFTY 50",
            "period": period,
            "assetsCompared": list(stock_dict.keys()),
            "chartPath": chart_path,
            "chartUrl": f"file://{chart_path}"
        }
