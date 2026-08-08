"""
Unit & Integration Tests for Phase 5 FastMCP Server & Tools Implementation.
"""

import pytest
from src.mcp_server.tools import (
    tool_search_indian_symbol,
    tool_fetch_financial_data,
    tool_analyze_and_visualize,
    tool_compare_assets,
)
from src.mcp_server.server import mcp


def test_mcp_server_initialization():
    assert mcp is not None
    assert mcp.name == "Arthra MCP"


def test_tool_search_indian_symbol():
    res = tool_search_indian_symbol("RELIANCE")
    assert res["query"] == "RELIANCE"
    assert res["resolvedStockSymbol"] == "RELIANCE.NS"
    assert res["stockQuoteSummary"] is not None


def test_tool_fetch_financial_data():
    res_stock = tool_fetch_financial_data("TCS", data_type="stock", period="1mo")
    assert res_stock["assetType"] == "Indian Stock"
    assert res_stock["candleCount"] > 0

    res_mf = tool_fetch_financial_data("122640", data_type="mutual_fund")
    assert res_mf["assetType"] == "Mutual Fund"
    assert res_mf["totalRecords"] > 0


def test_tool_analyze_and_visualize():
    res_stock = tool_analyze_and_visualize("HDFCBANK", asset_type="stock", period="3mo")
    assert res_stock["assetType"] == "Indian Stock"
    assert "technicalAnalysis" in res_stock
    assert "fundamentalScorecard" in res_stock
    assert res_stock["chartPath"] is not None

    res_mf = tool_analyze_and_visualize("122640", asset_type="mutual_fund")
    assert res_mf["assetType"] == "Mutual Fund"
    assert "quantitativeAnalysis" in res_mf
    assert res_mf["chartPath"] is not None


def test_tool_compare_assets():
    res_stock = tool_compare_assets(["RELIANCE", "TCS"], asset_type="stock", period="3mo")
    assert "comparisonType" in res_stock
    assert res_stock["chartPath"] is not None

    res_mf = tool_compare_assets(["122640", "125497"], asset_type="mutual_fund", period="6mo")
    assert "comparisonType" in res_mf
    assert res_mf["chartPath"] is not None


if __name__ == "__main__":
    pytest.main(["-v", __file__])
