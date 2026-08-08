"""
Arthra MCP — Main Application Entry Point.
Run FastMCP Server or launch interactive Financial Analyst Agent CLI.
"""

import sys
import argparse
import logging
from src.mcp_server.server import run_server
from src.agent.agent import FinancialAnalystAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ArthraMain")


def main():
    parser = argparse.ArgumentParser(
        description="Arthra MCP — Indian Stock & Mutual Fund Financial Analyst System"
    )
    parser.add_argument(
        "--server", action="store_true", help="Launch FastMCP Server over STDIO protocol"
    )
    parser.add_argument(
        "--agent", type=str, help="Run Financial Analyst Agent on a natural language query"
    )
    parser.add_argument(
        "--stock", type=str, help="Run complete financial analysis for an Indian stock (e.g. RELIANCE, TCS)"
    )
    parser.add_argument(
        "--mf", type=str, help="Run complete financial analysis for an Indian Mutual Fund (e.g. 122640, 'Parag Parikh')"
    )

    args = parser.parse_args()

    if args.server:
        run_server()
        return

    agent = FinancialAnalystAgent()

    if args.agent:
        res = agent.process_natural_language_query(args.agent)
        print("\n" + "=" * 75)
        print(f"✅ FINANCIAL REPORT GENERATED: {res.get('reportPath')}")
        print("=" * 75)
        print(res.get("reportMarkdown"))
        return

    if args.stock:
        res = agent.analyze_stock(args.stock)
        print("\n" + "=" * 75)
        print(f"✅ STOCK FINANCIAL REPORT GENERATED: {res.get('reportPath')}")
        print("=" * 75)
        print(res.get("reportMarkdown"))
        return

    if args.mf:
        res = agent.analyze_mutual_fund(args.mf)
        print("\n" + "=" * 75)
        print(f"✅ MUTUAL FUND REPORT GENERATED: {res.get('reportPath')}")
        print("=" * 75)
        print(res.get("reportMarkdown"))
        return

    # Interactive CLI Mode if no arguments supplied
    print("=" * 75)
    print("📈 WELCOME TO ARTHRA MCP — FINANCIAL ANALYST SYSTEM")
    print("=" * 75)
    print("Usage Options:")
    print("  python main.py --server                  # Run FastMCP Server")
    print("  python main.py --agent 'Analyze TCS'     # Analyze stock or mutual fund")
    print("  python main.py --stock RELIANCE          # Analyze stock")
    print("  python main.py --mf 122640               # Analyze mutual fund")
    print("=" * 75)
    
    query = input("\nEnter query (e.g., 'Analyze Reliance' or 'Analyze Parag Parikh Flexi Cap'): ").strip()
    if query:
        res = agent.process_natural_language_query(query)
        print("\n" + "=" * 75)
        print(f"✅ REPORT SAVED: {res.get('reportPath')}")
        print("=" * 75)
        print(res.get("reportMarkdown"))


if __name__ == "__main__":
    main()
