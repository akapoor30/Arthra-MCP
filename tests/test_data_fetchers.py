"""
Unit & Integration Tests for Phase 2 Data Ingestion Modules (stock_fetcher & mf_fetcher).
"""

import pytest
import pandas as pd
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


def test_symbol_normalization():
    assert normalize_indian_symbol("RELIANCE") == "RELIANCE.NS"
    assert normalize_indian_symbol("tcs.ns") == "TCS.NS"
    assert normalize_indian_symbol("500325.BO") == "500325.BO"


def test_get_stock_quote():
    quote = get_stock_quote("RELIANCE")
    assert quote["symbol"] in ["RELIANCE.NS", "RELIANCE.BO"]
    assert quote["currentPrice"] is not None
    assert quote["currentPrice"] > 0
    assert "currency" in quote
    assert quote["currency"] == "INR"


def test_get_historical_ohlcv():
    df = get_historical_ohlcv("TCS", period="1mo", interval="1d")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "Close" in df.columns
    assert len(df) > 5


def test_get_stock_fundamentals():
    fundamentals = get_stock_fundamentals("HDFCBANK")
    assert fundamentals["symbol"] in ["HDFCBANK.NS", "HDFCBANK.BO"]
    assert fundamentals["marketCap"] is not None


def test_search_mutual_fund():
    results = search_mutual_fund("Parag Parikh")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "schemeCode" in results[0]
    assert "schemeName" in results[0]


def test_get_mutual_fund_details_and_df():
    # Parag Parikh Flexi Cap Fund Direct Growth (122639 or search)
    results = search_mutual_fund("Parag Parikh Flexi Cap")
    scheme_code = results[0]["schemeCode"]
    
    details = get_mutual_fund_details(scheme_code)
    assert details["schemeCode"] == str(scheme_code)
    assert details["latestNav"] > 0
    
    df = get_mutual_fund_nav_df(scheme_code)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "nav" in df.columns


if __name__ == "__main__":
    pytest.main(["-v", __file__])
