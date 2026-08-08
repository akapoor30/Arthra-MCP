"""
Mutual Fund Quantitative Analytics & Risk Engine for Indian Funds.
Calculates CAGR (1Y/3Y/5Y/Inception), Rolling Returns, Volatility, Sharpe Ratio, Sortino Ratio, and Max Drawdown.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RBI / Indian 91-day T-Bill Risk-Free Benchmark ~6.5%
RBI_RISK_FREE_RATE = 0.065


def calculate_cagr(start_val: float, end_val: float, num_years: float) -> float:
    """Calculates Compound Annual Growth Rate (CAGR) as a percentage."""
    if start_val <= 0 or end_val <= 0 or num_years <= 0:
        return 0.0
    cagr = ((end_val / start_val) ** (1.0 / num_years)) - 1.0
    return round(float(cagr * 100.0), 2)


def calculate_max_drawdown(nav_series: pd.Series) -> Dict[str, Any]:
    """
    Calculates Maximum Drawdown (peak-to-trough peak percentage loss).
    """
    if nav_series.empty:
        return {"maxDrawdownPercent": 0.0, "peakDate": "", "troughDate": ""}
        
    cummax = nav_series.cummax()
    drawdown = (nav_series - cummax) / cummax
    max_dd = drawdown.min()
    
    trough_idx = drawdown.idxmin()
    peak_idx = nav_series.loc[:trough_idx].idxmax() if trough_idx in nav_series.index else nav_series.index[0]
    
    return {
        "maxDrawdownPercent": round(float(abs(max_dd) * 100.0), 2),
        "peakDate": str(peak_idx)[:10] if pd.notna(peak_idx) else "",
        "troughDate": str(trough_idx)[:10] if pd.notna(trough_idx) else ""
    }


def calculate_rolling_returns(nav_df: pd.DataFrame, rolling_window_days: int = 252) -> Dict[str, Any]:
    """
    Calculates 1-Year rolling returns across the entire NAV historical dataset.
    """
    if nav_df.empty or len(nav_df) < rolling_window_days:
        return {"averageRollingReturn": 0.0, "minRollingReturn": 0.0, "maxRollingReturn": 0.0, "positivePercentage": 0.0}
        
    nav_series = nav_df["nav"]
    rolling_ret = (nav_series.shift(-rolling_window_days) / nav_series - 1.0) * 100.0
    rolling_ret = rolling_ret.dropna()
    
    if rolling_ret.empty:
        return {"averageRollingReturn": 0.0, "minRollingReturn": 0.0, "maxRollingReturn": 0.0, "positivePercentage": 0.0}
        
    avg_ret = rolling_ret.mean()
    min_ret = rolling_ret.min()
    max_ret = rolling_ret.max()
    pos_pct = (rolling_ret > 0).mean() * 100.0
    
    return {
        "averageRollingReturn": round(float(avg_ret), 2),
        "minRollingReturn": round(float(min_ret), 2),
        "maxRollingReturn": round(float(max_ret), 2),
        "positivePercentage": round(float(pos_pct), 2)
    }


def analyze_mutual_fund_performance(
    nav_df: pd.DataFrame, risk_free_rate: float = RBI_RISK_FREE_RATE
) -> Dict[str, Any]:
    """
    Runs complete quantitative performance and risk analysis on mutual fund NAV DataFrame.
    """
    if nav_df.empty or "nav" not in nav_df.columns:
        return {"error": "Empty NAV DataFrame provided"}
        
    df = nav_df.sort_index().copy()
    navs = df["nav"]
    
    total_days = (df.index[-1] - df.index[0]).days
    total_years = total_days / 365.25
    
    current_nav = float(navs.iloc[-1])
    initial_nav = float(navs.iloc[0])
    
    # 1. Period CAGRs
    def get_cagr_for_days(days: int) -> Optional[float]:
        target_date = df.index[-1] - pd.Timedelta(days=days)
        sub = df.loc[df.index <= target_date]
        if sub.empty:
            return None
        start_n = float(sub["nav"].iloc[-1])
        yrs = days / 365.25
        return calculate_cagr(start_n, current_nav, yrs)

    cagr_1y = get_cagr_for_days(365)
    cagr_3y = get_cagr_for_days(365 * 3)
    cagr_5y = get_cagr_for_days(365 * 5)
    cagr_inception = calculate_cagr(initial_nav, current_nav, total_years) if total_years > 0.5 else 0.0

    # 2. Daily Returns & Risk Ratios
    daily_returns = navs.pct_change().dropna()
    ann_return = cagr_3y if cagr_3y is not None else cagr_inception
    ann_volatility = float(daily_returns.std() * np.sqrt(252) * 100.0) if len(daily_returns) > 20 else 0.0
    
    # Sharpe Ratio: (AnnReturn% - RiskFree%) / AnnVol%
    vol_frac = ann_volatility / 100.0
    ret_frac = (ann_return / 100.0) if ann_return else 0.0
    
    sharpe_ratio = ((ret_frac - risk_free_rate) / vol_frac) if vol_frac > 0 else 0.0
    
    # Sortino Ratio: (AnnReturn% - RiskFree%) / DownsideDev
    downside_returns = daily_returns[daily_returns < 0]
    downside_std = float(downside_returns.std() * np.sqrt(252)) if len(downside_returns) > 5 else vol_frac
    sortino_ratio = ((ret_frac - risk_free_rate) / downside_std) if downside_std > 0 else 0.0

    # 3. Max Drawdown & Rolling Returns
    mdd_dict = calculate_max_drawdown(navs)
    rolling_dict = calculate_rolling_returns(df, 252)

    return {
        "startDate": str(df.index[0])[:10],
        "endDate": str(df.index[-1])[:10],
        "totalYearsHistory": round(total_years, 2),
        "latestNav": round(current_nav, 4),
        "cagr1Y": cagr_1y if cagr_1y is not None else "N/A",
        "cagr3Y": cagr_3y if cagr_3y is not None else "N/A",
        "cagr5Y": cagr_5y if cagr_5y is not None else "N/A",
        "cagrInception": cagr_inception,
        "annualizedVolatility": round(ann_volatility, 2),
        "sharpeRatio": round(float(sharpe_ratio), 2),
        "sortinoRatio": round(float(sortino_ratio), 2),
        "maxDrawdown": mdd_dict,
        "rollingReturns1Y": rolling_dict
    }
