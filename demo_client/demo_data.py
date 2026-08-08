"""
Quick Demo Script to test Phase 2 Data Ingestion live with Indian Stocks and Mutual Funds.
"""

from src.data.stock_fetcher import get_stock_quote, get_stock_fundamentals, get_historical_ohlcv
from src.data.mf_fetcher import search_mutual_fund, get_mutual_fund_details, get_mutual_fund_nav_df


def main():
    print("=" * 70)
    print("🚀 ARTHRA MCP — PHASE 2 DATA INGESTION LIVE TEST")
    print("=" * 70)

    # 1. Test Indian Stock Data (Reliance Industries)
    stock_ticker = "RELIANCE"
    print(f"\n1. Fetching Live Quote for Stock: '{stock_ticker}'...")
    quote = get_stock_quote(stock_ticker)
    print(f"   Symbol: {quote['symbol']}")
    print(f"   Company: {quote['shortName']}")
    print(f"   Current Price: ₹{quote['currentPrice']:,.2f}")
    print(f"   Change: ₹{quote['change']} ({quote['percentChange']}%)")
    print(f"   52-Week High: ₹{quote.get('fiftyTwoWeekHigh', 0):,.2f}")
    print(f"   52-Week Low: ₹{quote.get('fiftyTwoWeekLow', 0):,.2f}")

    print(f"\n2. Fetching Fundamentals for: '{stock_ticker}'...")
    fundamentals = get_stock_fundamentals(stock_ticker)
    print(f"   Sector: {fundamentals.get('sector')}")
    print(f"   Industry: {fundamentals.get('industry')}")
    print(f"   P/E Ratio: {fundamentals.get('trailingPE')}")
    print(f"   P/B Ratio: {fundamentals.get('priceToBook')}")
    print(f"   ROE: {fundamentals.get('returnOnEquity')}")

    print(f"\n3. Fetching Historical OHLCV (1 Month) for: '{stock_ticker}'...")
    df_ohlcv = get_historical_ohlcv(stock_ticker, period="1mo")
    print(f"   Fetched {len(df_ohlcv)} daily candles.")
    print("   Recent Candles:")
    print(df_ohlcv.tail(3))

    # 2. Test Indian Mutual Fund Data (Parag Parikh Flexi Cap)
    mf_query = "Parag Parikh Flexi Cap"
    print(f"\n4. Searching Indian Mutual Funds for: '{mf_query}'...")
    mf_results = search_mutual_fund(mf_query)
    if mf_results:
        top_match = mf_results[0]
        scheme_code = top_match['schemeCode']
        scheme_name = top_match['schemeName']
        print(f"   Top Match Found: {scheme_name} (Code: {scheme_code})")

        print(f"\n5. Fetching Details & NAV History for Scheme Code: {scheme_code}...")
        mf_details = get_mutual_fund_details(scheme_code)
        print(f"   Fund House: {mf_details.get('fundHouse')}")
        print(f"   Category: {mf_details.get('schemeCategory')}")
        print(f"   Latest NAV: ₹{mf_details.get('latestNav')} (as of {mf_details.get('latestDate')})")

        nav_df = get_mutual_fund_nav_df(scheme_code)
        print(f"   Total Historical NAV records fetched: {len(nav_df)}")
        print("   Recent NAV History:")
        print(nav_df.tail(3))
    else:
        print("   No mutual fund scheme found.")

    print("\n" + "=" * 70)
    print("✅ LIVE TEST COMPLETED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    main()
