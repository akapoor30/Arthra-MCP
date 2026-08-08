"""
Live Demo Script to test Phase 5 FastMCP Tools & Server Functions.
Simulates MCP host calls for symbol resolution, data fetching, quantitative analysis, and comparisons.
"""

import json
from src.mcp_server.tools import (
    tool_search_indian_symbol,
    tool_fetch_financial_data,
    tool_analyze_and_visualize,
    tool_compare_assets,
)


def main():
    print("=" * 75)
    print("🚀 ARTHRA MCP — PHASE 5 FASTMCP TOOLS & SERVER DEMO")
    print("=" * 75)

    # 1. Test search_indian_symbol
    print("\n1. Invoking Tool: 'search_indian_symbol' for 'Parag Parikh'...")
    res_search = tool_search_indian_symbol("Parag Parikh")
    print(f"   Query: {res_search['query']}")
    print(f"   Resolved Stock Symbol: {res_search['resolvedStockSymbol']}")
    print("   Mutual Fund Matches Found:")
    for mf in res_search["mutualFundMatches"][:3]:
        print(f"     • {mf['schemeName']} (Code: {mf['schemeCode']})")

    # 2. Test analyze_and_visualize for stock (TCS)
    print("\n2. Invoking Tool: 'analyze_and_visualize' for Stock 'TCS'...")
    res_stock = tool_analyze_and_visualize("TCS", asset_type="stock", period="6mo")
    print(f"   Company: {res_stock['companyName']} ({res_stock['symbol']})")
    print(f"   Technical Sentiment: {res_stock['technicalAnalysis']['sentiment']}")
    print(f"   RSI (14): {res_stock['technicalAnalysis']['rsi']}")
    print(f"   Financial Health Score: {res_stock['fundamentalScorecard']['healthScore']}/100")
    print(f"   Rating: {res_stock['fundamentalScorecard']['scoreRating']}")
    print(f"   Generated Interactive Chart: {res_stock['chartPath']}")

    # 3. Test analyze_and_visualize for Mutual Fund (122640)
    print("\n3. Invoking Tool: 'analyze_and_visualize' for Mutual Fund Code '122640'...")
    res_mf = tool_analyze_and_visualize("122640", asset_type="mutual_fund")
    quant = res_mf["quantitativeAnalysis"]
    print(f"   Scheme: {res_mf['schemeName']} ({res_mf['schemeCode']})")
    print(f"   Category: {res_mf['category']}")
    print(f"   CAGR Since Inception: {quant['cagrInception']}%")
    print(f"   Sharpe Ratio: {quant['sharpeRatio']}")
    print(f"   Max Drawdown: -{quant['maxDrawdown']['maxDrawdownPercent']}%")
    print(f"   Generated Interactive Chart: {res_mf['chartPath']}")

    # 4. Test compare_assets for stocks
    print("\n4. Invoking Tool: 'compare_assets' for Indian Equities...")
    res_compare = tool_compare_assets(["RELIANCE", "TCS", "HDFCBANK"], asset_type="stock", period="1y")
    print(f"   Comparison Type: {res_compare['comparisonType']}")
    print(f"   Assets Compared: {', '.join(res_compare['assetsCompared'])}")
    print(f"   Generated Interactive Comparison Chart: {res_compare['chartPath']}")

    print("\n" + "=" * 75)
    print("✅ PHASE 5 FASTMCP SERVER DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 75)


if __name__ == "__main__":
    main()
