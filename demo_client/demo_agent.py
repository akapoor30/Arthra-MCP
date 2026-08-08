"""
Live Demo Script to test Phase 6 Financial Analyst Agent & CLI Entry Point.
Executes complete stock and mutual fund research workflows and generates structured Markdown reports.
"""

from src.agent.agent import FinancialAnalystAgent


def main():
    print("=" * 75)
    print("🚀 ARTHRA MCP — PHASE 6 FINANCIAL ANALYST AGENT DEMO")
    print("=" * 75)

    agent = FinancialAnalystAgent()

    # 1. Test Agent Stock Analysis (Tata Consultancy Services)
    print("\n1. Running Agent Stock Analysis for 'TCS'...")
    res_stock = agent.analyze_stock("TCS", period="1y")
    print(f"   Company: {res_stock['companyName']} ({res_stock['symbol']})")
    print(f"   Generated Markdown Report: {res_stock['reportPath']}")

    # 2. Test Agent Mutual Fund Analysis (Parag Parikh Flexi Cap)
    print("\n2. Running Agent Mutual Fund Analysis for Scheme Code '122640'...")
    res_mf = agent.analyze_mutual_fund("122640")
    print(f"   Scheme: {res_mf['schemeName']} ({res_mf['schemeCode']})")
    print(f"   Generated Markdown Report: {res_mf['reportPath']}")

    # 3. Test Natural Language Query Processing
    print("\n3. Processing Natural Language Query: 'Analyze Reliance Industries'...")
    res_nl = agent.process_natural_language_query("Analyze Reliance Industries")
    print(f"   Report Path: {res_nl['reportPath']}")

    print("\n" + "=" * 75)
    print("✅ PHASE 6 AGENT DEMO COMPLETED SUCCESSFULLY!")
    print("   Generated Markdown Reports saved in reports/:")
    print(f"   • {res_stock['reportPath']}")
    print(f"   • {res_mf['reportPath']}")
    print(f"   • {res_nl['reportPath']}")
    print("=" * 75)


if __name__ == "__main__":
    main()
