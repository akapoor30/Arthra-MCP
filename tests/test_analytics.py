"""
Unit Tests for Phase 3 Quantitative & Financial Analytics Engine.
"""

import pytest
import pandas as pd
import numpy as np
from src.analytics.technicals import (
    calculate_sma,
    calculate_ema,
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands,
    get_full_technical_analysis,
)
from src.analytics.fundamentals import compute_financial_health_scorecard
from src.analytics.mf_analytics import (
    calculate_cagr,
    calculate_max_drawdown,
    analyze_mutual_fund_performance,
)


@pytest.fixture
def sample_ohlcv_df():
    """Generates a synthetic 100-day OHLCV price series for testing."""
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=100, freq="D")
    price = 100.0 + np.cumsum(np.random.randn(100) * 2.0)
    price = np.maximum(price, 10.0)  # Avoid negative values
    
    df = pd.DataFrame({
        "Open": price * 0.99,
        "High": price * 1.02,
        "Low": price * 0.98,
        "Close": price,
        "Volume": np.random.randint(100000, 5000000, size=100)
    }, index=dates)
    return df


def test_technical_indicators(sample_ohlcv_df):
    sma20 = calculate_sma(sample_ohlcv_df, 20)
    assert len(sma20) == 100
    assert not pd.isna(sma20.iloc[-1])

    rsi = calculate_rsi(sample_ohlcv_df, 14)
    assert 0 <= rsi.iloc[-1] <= 100

    macd_dict = calculate_macd(sample_ohlcv_df)
    assert "macd" in macd_dict
    assert "signal" in macd_dict
    assert "histogram" in macd_dict

    bb_dict = calculate_bollinger_bands(sample_ohlcv_df)
    assert bb_dict["upper"].iloc[-1] >= bb_dict["middle"].iloc[-1]
    assert bb_dict["middle"].iloc[-1] >= bb_dict["lower"].iloc[-1]


def test_full_technical_analysis(sample_ohlcv_df):
    ta_res = get_full_technical_analysis(sample_ohlcv_df)
    assert "rsi" in ta_res
    assert "overallSentiment" in ta_res
    assert ta_res["overallSentiment"] in ["STRONG BULLISH", "BULLISH", "NEUTRAL", "BEARISH", "STRONG BEARISH"]


def test_fundamental_scorecard():
    fund_data = {
        "symbol": "RELIANCE.NS",
        "companyName": "Reliance Industries",
        "trailingPE": 22.5,
        "priceToBook": 2.1,
        "returnOnEquity": 0.15,
        "revenueGrowth": 0.10,
        "earningsGrowth": 0.12,
        "debtToEquity": 45.0
    }
    scorecard = compute_financial_health_scorecard(fund_data)
    assert 0 <= scorecard["healthScore"] <= 100
    assert "scoreRating" in scorecard
    assert "valuationStatus" in scorecard


def test_mf_analytics():
    cagr = calculate_cagr(100.0, 200.0, 3.0)
    assert cagr == round(((2.0 ** (1/3)) - 1) * 100, 2)

    # Generate synthetic NAV DataFrame
    dates = pd.date_range(start="2023-01-01", periods=1000, freq="D")
    nav_series = 10.0 * np.exp(np.linspace(0, 0.5, 1000))
    nav_df = pd.DataFrame({"nav": nav_series}, index=dates)

    analysis = analyze_mutual_fund_performance(nav_df)
    assert analysis["totalYearsHistory"] > 2.5
    assert analysis["sharpeRatio"] is not None
    assert "maxDrawdown" in analysis


if __name__ == "__main__":
    pytest.main(["-v", __file__])
