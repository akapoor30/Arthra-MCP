"""
Unit & Integration Tests for Phase 6 Financial Analyst Agent & CLI Entry Point.
"""

import os
import pytest
from src.agent.agent import FinancialAnalystAgent


def test_agent_initialization():
    agent = FinancialAnalystAgent()
    assert agent.name == "Arthra Financial Analyst"


def test_analyze_stock():
    agent = FinancialAnalystAgent()
    res = agent.analyze_stock("RELIANCE", period="3mo")
    assert res["symbol"] == "RELIANCE.NS"
    assert os.path.exists(res["reportPath"])
    assert os.path.getsize(res["reportPath"]) > 500
    assert "Financial Research Report" in res["reportMarkdown"]


def test_analyze_mutual_fund():
    agent = FinancialAnalystAgent()
    res = agent.analyze_mutual_fund("122640")
    assert res["schemeCode"] == "122640"
    assert os.path.exists(res["reportPath"])
    assert os.path.getsize(res["reportPath"]) > 500
    assert "Mutual Fund Performance Report" in res["reportMarkdown"]


def test_process_natural_language_query():
    agent = FinancialAnalystAgent()
    res_stock = agent.process_natural_language_query("Analyze TCS")
    assert "TCS.NS" in res_stock["symbol"]

    res_mf = agent.process_natural_language_query("Analyze Parag Parikh Flexi Cap Fund")
    assert "Mutual Fund" in res_mf["analysis"]["assetType"]


if __name__ == "__main__":
    pytest.main(["-v", __file__])
