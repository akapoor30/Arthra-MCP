"""
Unit & Integration Tests for Phase 4 Plotly Visualization Engine.
"""

import os
import pytest
from src.visualization.chart_builder import (
    build_stock_technical_chart,
    build_mutual_fund_chart,
    build_stock_comparison_chart,
    build_mutual_fund_comparison_chart,
    CHARTS_DIR,
)


def test_build_stock_technical_chart():
    filepath = build_stock_technical_chart("RELIANCE", period="3mo", save_filename="test_stock_tech.html")
    assert os.path.exists(filepath)
    assert os.path.getsize(filepath) > 1000
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        assert "plotly" in content.lower()
        assert "RELIANCE.NS" in content


def test_build_mutual_fund_chart():
    filepath = build_mutual_fund_chart(122640, save_filename="test_mf_chart.html")
    assert os.path.exists(filepath)
    assert os.path.getsize(filepath) > 1000
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        assert "plotly" in content.lower()


def test_build_stock_comparison_chart():
    stocks = {
        "Reliance": "RELIANCE",
        "TCS": "TCS.NS"
    }
    filepath = build_stock_comparison_chart(stocks, period="3mo", save_filename="test_stock_compare.html")
    assert os.path.exists(filepath)
    assert os.path.getsize(filepath) > 1000
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        assert "NIFTY 50 Benchmark" in content


def test_build_mutual_fund_comparison_chart():
    mfs = {
        "Parag Parikh Flexi Cap": 122640,
        "SBI Small Cap": 125497
    }
    filepath = build_mutual_fund_comparison_chart(mfs, period="1y", save_filename="test_mf_compare.html")
    assert os.path.exists(filepath)
    assert os.path.getsize(filepath) > 1000
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        assert "NIFTY 50 Benchmark" in content


if __name__ == "__main__":
    pytest.main(["-v", __file__])
