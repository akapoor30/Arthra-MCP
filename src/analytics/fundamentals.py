"""
Fundamental Analysis & Financial Scorecard Engine for Indian Stocks.
Evaluates valuation ratios, profitability metrics, debt leverage, liquidity, and overall financial health.
"""

from typing import Dict, Any, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def evaluate_valuation_status(trailing_pe: Optional[float], price_to_book: Optional[float], sector: str = "") -> str:
    """
    Evaluates stock valuation relative to general Indian market standards.
    """
    if trailing_pe is None or trailing_pe <= 0:
        return "UNVALUED / NEGATIVE EARNINGS"
        
    if trailing_pe < 15:
        return "ATTRACTIVE / UNDERVALUED"
    elif 15 <= trailing_pe <= 28:
        return "FAIR / FAIRLY VALUED"
    elif 28 < trailing_pe <= 50:
        return "PREMIUM / EXPENSIVE"
    else:
        return "VERY HIGH VALUATION"


def compute_financial_health_scorecard(fundamentals_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculates a 100-point fundamental scorecard assessing Valuation, Profitability, Growth, and Financial Stability.
    """
    score = 0
    max_score = 100
    breakdown = []
    
    pe = fundamentals_dict.get("trailingPE")
    pb = fundamentals_dict.get("priceToBook")
    roe = fundamentals_dict.get("returnOnEquity")
    roa = fundamentals_dict.get("returnOnAssets")
    profit_margin = fundamentals_dict.get("profitMargins")
    rev_growth = fundamentals_dict.get("revenueGrowth")
    eps_growth = fundamentals_dict.get("earningsGrowth")
    debt_equity = fundamentals_dict.get("debtToEquity")
    current_ratio = fundamentals_dict.get("currentRatio")
    
    # 1. Valuation Pillar (Max 25 pts)
    if pe is not None and pe > 0:
        if pe < 20:
            score += 25
            breakdown.append("Valuation: Excellent (P/E < 20) [+25 pts]")
        elif pe <= 35:
            score += 18
            breakdown.append("Valuation: Moderate (P/E 20-35) [+18 pts]")
        else:
            score += 10
            breakdown.append("Valuation: High P/E (> 35) [+10 pts]")
    else:
        score += 10
        breakdown.append("Valuation: N/A [+10 pts]")
        
    # 2. Profitability Pillar (ROE/ROA/Margin - Max 25 pts)
    if roe is not None and roe > 0:
        if roe >= 0.18:  # >= 18% ROE
            score += 25
            breakdown.append(f"Profitability: Superior ROE ({roe*100:.1f}%) [+25 pts]")
        elif roe >= 0.12:  # >= 12% ROE
            score += 18
            breakdown.append(f"Profitability: Solid ROE ({roe*100:.1f}%) [+18 pts]")
        else:
            score += 10
            breakdown.append(f"Profitability: Modest ROE ({roe*100:.1f}%) [+10 pts]")
    else:
        score += 12
        breakdown.append("Profitability: ROE Data N/A [+12 pts]")

    # 3. Growth Pillar (Revenue & Earnings Growth - Max 25 pts)
    growth_score = 0
    if rev_growth is not None and rev_growth > 0:
        growth_score += 12.5
    if eps_growth is not None and eps_growth > 0:
        growth_score += 12.5
        
    score += int(growth_score)
    breakdown.append(f"Growth Score: [+{int(growth_score)} pts]")
    
    # 4. Solvency & Debt Balance (Max 25 pts)
    if debt_equity is not None:
        if debt_equity < 50:  # Low debt (< 0.5 D/E)
            score += 25
            breakdown.append("Solvency: Low Leverage / Debt-Free (< 0.5 D/E) [+25 pts]")
        elif debt_equity <= 100:  # Moderate debt (< 1.0 D/E)
            score += 18
            breakdown.append("Solvency: Moderate Debt (0.5 - 1.0 D/E) [+18 pts]")
        else:
            score += 8
            breakdown.append("Solvency: High Debt (> 1.0 D/E) [+8 pts]")
    else:
        score += 15
        breakdown.append("Solvency: D/E N/A [+15 pts]")
        
    # Overall Assessment
    if score >= 80:
        rating = "STRONG FUNDAMENTALS (BUY CANDIDATE)"
    elif score >= 60:
        rating = "MODERATE / FAIR FUNDAMENTALS"
    elif score >= 40:
        rating = "WEAK FUNDAMENTALS (EXERCISE CAUTION)"
    else:
        rating = "HIGH RISK / POOR FUNDAMENTALS"
        
    valuation_status = evaluate_valuation_status(pe, pb, fundamentals_dict.get("sector", ""))

    return {
        "symbol": fundamentals_dict.get("symbol"),
        "companyName": fundamentals_dict.get("companyName"),
        "healthScore": score,
        "maxScore": max_score,
        "scoreRating": rating,
        "valuationStatus": valuation_status,
        "trailingPE": pe,
        "priceToBook": pb,
        "roePercent": round(roe * 100, 2) if roe else None,
        "roaPercent": round(roa * 100, 2) if roa else None,
        "profitMarginPercent": round(profit_margin * 100, 2) if profit_margin else None,
        "debtToEquity": debt_equity,
        "currentRatio": current_ratio,
        "scoreBreakdown": breakdown
    }
