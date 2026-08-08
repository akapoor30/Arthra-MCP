"""
FastMCP Server Implementation for Arthra MCP.
Exposes Model Context Protocol tools over STDIO transport protocol.
"""

from typing import Dict, Any, List, Optional
import sys
import logging
from mcp.server.mcpserver import MCPServer
from src.mcp_server.tools import (
    tool_search_indian_symbol,
    tool_fetch_financial_data,
    tool_analyze_and_visualize,
    tool_compare_assets,
)

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("ArthraMCPServer")

# Initialize FastMCP / MCPServer Instance
mcp = MCPServer("Arthra MCP")


@mcp.tool()
def search_indian_symbol(query: str) -> Dict[str, Any]:
    """
    Resolves an Indian stock symbol or searches AMFI Mutual Fund scheme codes.
    
    Args:
        query: Company name or keyword (e.g., 'RELIANCE', 'TCS', 'Parag Parikh')
    """
    return tool_search_indian_symbol(query)


@mcp.tool()
def fetch_financial_data(
    symbol: str, data_type: str = "stock", period: str = "1y"
) -> Dict[str, Any]:
    """
    Fetches raw financial market data for Indian Stocks or Mutual Funds.
    
    Args:
        symbol: Stock symbol ('RELIANCE') or Mutual Fund scheme code ('122640')
        data_type: 'stock', 'mutual_fund', 'fundamentals', or 'financials'
        period: Time period ('1mo', '3mo', '6mo', '1y', '2y', '5y')
    """
    return tool_fetch_financial_data(symbol, data_type=data_type, period=period)


@mcp.tool()
def analyze_and_visualize(
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
    return tool_analyze_and_visualize(symbol, asset_type=asset_type, period=period, generate_chart=generate_chart)


@mcp.tool()
def compare_assets(
    assets: List[str], asset_type: str = "stock", period: str = "1y"
) -> Dict[str, Any]:
    """
    Compares performance of multiple Indian stocks or mutual funds vs NIFTY 50 benchmark on a 0% baseline.
    
    Args:
        assets: List of symbols (e.g. ['RELIANCE', 'TCS', 'HDFCBANK']) or Scheme Codes (e.g. ['122640', '125497'])
        asset_type: 'stock' or 'mutual_fund'
        period: Time period ('3mo', '6mo', '1y', '3y', '5y')
    """
    return tool_compare_assets(assets, asset_type=asset_type, period=period)


def run_server():
    """Launches the Arthra FastMCP server over STDIO transport."""
    logger.info("🚀 Starting Arthra MCP Server over STDIO...")
    mcp.run()


if __name__ == "__main__":
    run_server()
