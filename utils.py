"""
Utility functions for text processing, extraction, and validation.
"""

import re
from typing import Optional

import pandas as pd
from nltk.stem import PorterStemmer

# Initialize stemmer
ps = PorterStemmer()


def clean_text(text: str) -> str:
    """
    Clean and preprocess text for model prediction.

    Args:
        text: Raw text to clean

    Returns:
        Cleaned and preprocessed text
    """
    if text is None or pd.isna(text):
        return ""

    text = str(text)

    # Remove "Read more" and similar patterns from scraped reviews
    text = re.sub(r"\s*read\s+more\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*\.\.\.\s*read\s+more\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*see\s+more\s*$", "", text, flags=re.IGNORECASE)

    # Remove URLs
    text = re.sub(r"http\S+", " ", text)
    # Remove special characters
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    # Lowercase
    text = text.lower()
    # Stemming
    words = [ps.stem(word) for word in text.split()]

    return " ".join(words)


def remove_read_more_patterns(text: str) -> str:
    """Remove 'read more' and similar patterns from text."""
    text = re.sub(r"\s*read\s+more\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*\.\.\.\s*read\s+more\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*see\s+more\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*(?:\.\.\.|\.)\s*$", "", text)
    return text.strip()


def extract_asin_from_url(url: str) -> Optional[str]:
    """
    Extract ASIN from Amazon URL.

    Args:
        url: Amazon product URL or ASIN code

    Returns:
        ASIN code if found, None otherwise
    """
    patterns = [
        r"/dp/([A-Z0-9]{10})",
        r"/d/([A-Z0-9]{10})",
        r"/product/([A-Z0-9]{10})",
        r"[?&]asin=([A-Z0-9]{10})",
        r"/gp/product/([A-Z0-9]{10})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # Check if URL is already an ASIN
    if re.match(r"^[A-Z0-9]{10}$", url.strip()):
        return url.strip()

    return None


def extract_product_id_from_walmart_url(url: str) -> Optional[str]:
    """
    Extract product ID from Walmart URL.

    Args:
        url: Walmart product URL or product ID

    Returns:
        Product ID if found, None otherwise
    """
    patterns = [
        r"/ip/[^/]+/(\d+)",  # /ip/Product-Name/12345678901
        r"/[^/]*product[^/]*/(\d+)",  # variations
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # Check if URL is already a product ID (numeric)
    if re.match(r"^\d+$", url.strip()):
        return url.strip()

    return None


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to max length with ellipsis.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def detect_review_column(df: pd.DataFrame, possible_columns: list) -> Optional[str]:
    """
    Auto-detect review column from DataFrame.

    Args:
        df: DataFrame to inspect
        possible_columns: List of possible column names

    Returns:
        Column name if found, None otherwise
    """
    for col in possible_columns:
        if col in df.columns:
            return col
    return None


def format_confidence(confidence: Optional[float]) -> str:
    """
    Format confidence value as percentage string.

    Args:
        confidence: Confidence value (0-1)

    Returns:
        Formatted percentage string
    """
    if confidence is None:
        return "N/A"
    return f"{confidence * 100:.1f}%"


def format_metric(value, decimal_places: int = 4) -> str:
    """
    Format metric value.

    Args:
        value: Metric value
        decimal_places: Number of decimal places

    Returns:
        Formatted metric string
    """
    if isinstance(value, float):
        return f"{value:.{decimal_places}f}"
    return str(value)
