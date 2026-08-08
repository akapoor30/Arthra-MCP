"""
Live Demo Script to test Phase 3 Quantitative Analytics Engine on real Indian Stocks & Mutual Funds.
"""

from src.data.stock_fetcher import get_historical_ohlcv, get_stock_fundamentals
from src.data.mf_fetcher import search_mutual_fund, get_mutual_fund_nav_df
from src.analytics.technicals import get_full_technical_analysis, calculate_beta_and_volatility
from src.analytics.fundamentals import compute_financial_health_scorecard
from src.analytics.mf_analytics import analyze_mutual_fund_performance


def main():
    print("=" * 75)
    print("🚀 ARTHRA MCP — PHASE 3 QUANTITATIVE ANALYTICS ENGINE DEMO")
    print("=" * 75)

    # 1. Stock Technical & Fundamental Analytics (TCS)
    ticker = "TCS"
    print(f"\n1. Running Quantitative Technical Analysis for Stock: '{ticker}'...")
    df_ohlcv = get_historical_ohlcv(ticker, period="1y")
    ta_res = get_full_technical_analysis(df_ohlcv)
    beta_res = calculate_beta_and_volatility(df_ohlcv)

    print(f"   Latest Close: ₹{ta_res['latestClose']}")
    print(f"   Overall Technical Sentiment: {ta_res['overallSentiment']}")
    print(f"   RSI (14): {ta_res['rsi']}")
    print(f"   SMA 20: ₹{ta_res['sma20']} | SMA 50: ₹{ta_res['sma50']} | SMA 200: ₹{ta_res['sma200']}")
    print(f"   MACD Line: {ta_res['macd']} | Signal: {ta_res['macdSignal']} | Hist: {ta_res['macdHist']}")
    print(f"   Annualized Volatility: {beta_res['volatility']}% | Beta vs NIFTY 50: {beta_res['beta']}")
    print("   Signal Highlights:")
    for sig in ta_res["signalHighlights"]:
        print(f"     • {sig}")

    print(f"\n2. Running Fundamental Scorecard for Stock: '{ticker}'...")
    fund_raw = get_stock_fundamentals(ticker)
    scorecard = compute_financial_health_scorecard(fund_raw)
    print(f"   Financial Health Score: {scorecard['healthScore']}/100")
    print(f"   Rating: {scorecard['scoreRating']}")
    print(f"   Valuation Status: {scorecard['valuationStatus']}")
    print(f"   P/E Ratio: {scorecard.get('trailingPE')} | P/B: {scorecard.get('priceToBook')}")
    print(f"   ROE: {scorecard.get('roePercent')}% | Debt-to-Equity: {scorecard.get('debtToEquity')}")
    print("   Score Breakdown:")
    for bd in scorecard["scoreBreakdown"]:
        print(f"     • {bd}")

    # 2. Mutual Fund Quantitative Risk/Return Analysis
    mf_query = "SBI Small Cap"
    print(f"\n3. Running Mutual Fund Analytics for: '{mf_query}'...")
    mf_search = search_mutual_fund(mf_query)
    if mf_search:
        scheme_code = mf_search[0]["schemeCode"]
        scheme_name = mf_search[0]["schemeName"]
        print(f"   Found Scheme: {scheme_name} (Code: {scheme_code})")
        
        nav_df = get_mutual_fund_nav_df(scheme_code)
        mf_analysis = analyze_mutual_fund_performance(nav_df)

        print(f"   History Analyzed: {mf_analysis['totalYearsHistory']} years ({mf_analysis['startDate']} to {mf_analysis['endDate']})")
        print(f"   Latest NAV: ₹{mf_analysis['latestNav']}")
        print(f"   CAGR 1-Year: {mf_analysis['cagr1Y']}%")
        print(f"   CAGR 3-Year: {mf_analysis['cagr3Y']}%")
        print(f"   CAGR 5-Year: {mf_analysis['cagr5Y']}%")
        print(f"   CAGR Since Inception: {mf_analysis['cagrInception']}%")
        print(f"   Annualized Volatility: {mf_analysis['annualizedVolatility']}%")
        print(f"   Sharpe Ratio: {mf_analysis['sharpeRatio']} (vs RBI 6.5% T-Bill benchmark)")
        print(f"   Sortino Ratio: {mf_analysis['sortinoRatio']}")
        
        mdd = mf_analysis["maxDrawdown"]
        print(f"   Max Drawdown: -{mdd['maxDrawdownPercent']}% (Peak: {mdd['peakDate']} → Trough: {mdd['troughDate']})")
        
        roll = mf_analysis["rollingReturns1Y"]
        print(f"   1-Year Rolling Returns: Avg: {roll['averageRollingReturn']}% | Min: {roll['minRollingReturn']}% | Max: {roll['maxRollingReturn']}% | Positive Years: {roll['positivePercentage']}%")

    print("\n" + "=" * 75)
    print("✅ PHASE 3 QUANTITATIVE ENGINE DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 75)


if __name__ == "__main__":
    main()
