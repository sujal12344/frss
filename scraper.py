"""
Web scraping and API integration functionality.
"""

from typing import Any, Dict, Optional

import requests
import streamlit as st

from config import AMAZON_API_URL, API_TIMEOUT, SCRAPER_API_KEY, WALMART_API_URL


def fetch_amazon_reviews(asin: str) -> Optional[Dict[str, Any]]:
    """
    Fetch product reviews from Amazon using ScraperAPI.

    Args:
        asin: Amazon Standard Identification Number

    Returns:
        Dictionary with product data and reviews, or None on error
    """
    try:
        payload = {"api_key": SCRAPER_API_KEY, "asin": asin}

        with st.spinner(f"🔄 Fetching reviews for ASIN: {asin}..."):
            response = requests.get(
                AMAZON_API_URL,
                params=payload,
                timeout=API_TIMEOUT,
            )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.error("❌ Product not found on Amazon!")
            return None
        else:
            st.error(f"❌ API Error: Status Code {response.status_code}")
            print(f"API Error: {response.text}")
            return None

    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
        print(f"Exception: {str(e)}")
        return None


def fetch_walmart_reviews(product_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch product reviews from Walmart using ScraperAPI.

    Args:
        product_id: Walmart product ID

    Returns:
        Dictionary with product data and reviews, or None on error
    """
    try:
        payload = {"api_key": SCRAPER_API_KEY, "product_id": product_id}

        with st.spinner(f"🔄 Fetching reviews for Product ID: {product_id}..."):
            response = requests.get(
                WALMART_API_URL,
                params=payload,
                timeout=API_TIMEOUT,
            )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.error("❌ Product not found on Walmart!")
            return None
        else:
            st.error(f"❌ API Error: Status Code {response.status_code}")
            print(f"API Error: {response.text}")
            return None

    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
        print(f"Exception: {str(e)}")
        return None
        st.error(f"❌ Error fetching data: {str(e)}")
        print(f"Exception: {str(e)}")
        return None
