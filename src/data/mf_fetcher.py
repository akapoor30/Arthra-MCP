"""
Mutual Fund Data Fetcher Module for Indian Funds (AMFI API / mfapi.in).
Searches mutual fund scheme codes and parses historical NAV time-series data.
"""

from typing import Dict, Any, List, Optional
import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_MF_API = "https://api.mfapi.in/mf"


def search_mutual_fund(query: str) -> List[Dict[str, Any]]:
    """
    Searches Indian Mutual Fund schemes matching a query string.
    """
    logger.info(f"Searching Indian Mutual Funds for query: '{query}'")
    url = f"{BASE_MF_API}/search"
    params = {"q": query}
    
    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        results = response.json()
        return results if isinstance(results, list) else []
    except Exception as e:
        logger.error(f"Error searching mutual funds for '{query}': {e}")
        return []


def get_mutual_fund_details(scheme_code: str | int) -> Dict[str, Any]:
    """
    Fetches scheme details, metadata, and historical NAV series for an Indian Mutual Fund scheme code.
    """
    code_str = str(scheme_code).strip()
    logger.info(f"Fetching Mutual Fund details for Scheme Code: {code_str}")
    url = f"{BASE_MF_API}/{code_str}"
    
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        meta = data.get("meta", {})
        nav_list = data.get("data", [])
        
        if not nav_list:
            raise ValueError(f"No NAV history found for scheme code {code_str}")

        # Latest NAV & Date
        latest_entry = nav_list[0] if nav_list else {}
        latest_nav = float(latest_entry.get("nav", 0.0))
        latest_date = latest_entry.get("date", "")
        
        return {
            "schemeCode": str(meta.get("scheme_code") or code_str),
            "schemeName": meta.get("scheme_name", "Unknown Scheme"),
            "fundHouse": meta.get("fund_house", "Unknown Fund House"),
            "schemeCategory": meta.get("scheme_category", "Unknown Category"),
            "schemeType": meta.get("scheme_type", "Open Ended"),
            "latestNav": latest_nav,
            "latestDate": latest_date,
            "rawNavData": nav_list
        }
    except Exception as e:
        logger.error(f"Error fetching mutual fund details for scheme code '{code_str}': {e}")
        return {
            "error": str(e),
            "schemeCode": code_str,
            "schemeName": "Unknown Scheme",
            "rawNavData": []
        }


def get_mutual_fund_nav_df(scheme_code: str | int) -> pd.DataFrame:
    """
    Fetches and transforms mutual fund NAV history into a clean Pandas DataFrame sorted chronologically.
    
    Args:
        scheme_code: AMFI Scheme Code (e.g. 122639)
        
    Returns:
        pd.DataFrame with datetime index 'date' and float column 'nav'.
    """
    details = get_mutual_fund_details(scheme_code)
    nav_list = details.get("rawNavData", [])
    
    if not nav_list:
        return pd.DataFrame(columns=["nav"])

    # Build DataFrame
    df = pd.DataFrame(nav_list)
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    df.dropna(subset=["nav"], inplace=True)
    
    # Sort chronologically (oldest to newest)
    df.sort_values(by="date", inplace=True)
    df.set_index("date", inplace=True)
    
    return df[["nav"]]
