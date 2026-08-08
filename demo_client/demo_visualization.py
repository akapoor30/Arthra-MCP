"""
Live Demo Script to test Phase 4 Plotly Visualization Engine on real Indian Stocks & Mutual Funds.
Generates separate interactive HTML charts for Stocks and Mutual Funds saved in the charts/ directory.
"""

from src.visualization.chart_builder import (
    build_stock_technical_chart,
    build_mutual_fund_chart,
    build_stock_comparison_chart,
    build_mutual_fund_comparison_chart,
)


def main():
    print("=" * 75)
    print("🚀 ARTHRA MCP — PHASE 4 PLOTLY VISUALIZATION ENGINE DEMO")
    print("=" * 75)

    # 1. Generate Stock Candlestick Technical Chart (Reliance Industries)
    stock_ticker = "RELIANCE"
    print(f"\n1. Generating 3-Panel Technical Candlestick Chart for Stock: '{stock_ticker}'...")
    stock_chart_path = build_stock_technical_chart(stock_ticker, period="1y")
    print(f"   ✅ Saved Stock Technical Chart: {stock_chart_path}")

    # 2. Generate Mutual Fund Performance & Drawdown Chart (Parag Parikh Flexi Cap)
    scheme_code = 122640
    print(f"\n2. Generating NAV Trajectory & Drawdown Chart for Mutual Fund Code: {scheme_code}...")
    mf_chart_path = build_mutual_fund_chart(scheme_code)
    print(f"   ✅ Saved Mutual Fund Chart: {mf_chart_path}")

    # 3. Generate Stock vs Stock Comparison Chart (vs NIFTY 50)
    stocks = {
        "Reliance Industries": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "HDFC Bank": "HDFCBANK.NS"
    }
    print("\n3. Generating Stocks Comparison Chart (Reliance vs TCS vs HDFC Bank vs NIFTY 50)...")
    stock_compare_path = build_stock_comparison_chart(stocks, period="1y")
    print(f"   ✅ Saved Stock Comparison Chart: {stock_compare_path}")

    # 4. Generate Mutual Fund vs Mutual Fund Comparison Chart (vs NIFTY 50)
    mutual_funds = {
        "Parag Parikh Flexi Cap": 122640,
        "SBI Small Cap": 125497
    }
    print("\n4. Generating Mutual Funds Comparison Chart (PPFC vs SBI Small Cap vs NIFTY 50)...")
    mf_compare_path = build_mutual_fund_comparison_chart(mutual_funds, period="1y")
    print(f"   ✅ Saved Mutual Fund Comparison Chart: {mf_compare_path}")

    print("\n" + "=" * 75)
    print("✅ PHASE 4 VISUALIZATION DEMO COMPLETED SUCCESSFULLY!")
    print("   Open the separate HTML files in your browser to inspect:")
    print(f"   • Stock Technical:   {stock_chart_path}")
    print(f"   • Mutual Fund Performance: {mf_chart_path}")
    print(f"   • Stocks Comparison: {stock_compare_path}")
    print(f"   • MF Comparison:     {mf_compare_path}")
    print("=" * 75)


if __name__ == "__main__":
    main()
