import pandas as pd

from utils import (
    clean_text,
    detect_review_column,
    extract_asin_from_url,
    extract_product_id_from_walmart_url,
    format_confidence,
    format_metric,
    remove_read_more_patterns,
    truncate_text,
)


def test_clean_text_removes_noise_and_urls():
    text = "This PRODUCT is amazing!!! http://example.com ... Read more"
    cleaned = clean_text(text)
    assert "http" not in cleaned
    assert "read more" not in cleaned
    assert cleaned == cleaned.lower()


def test_remove_read_more_patterns():
    assert remove_read_more_patterns("Great quality ... read more") == "Great quality"
    assert remove_read_more_patterns("Works fine see more") == "Works fine"


def test_extract_asin_from_url_and_direct_value():
    assert extract_asin_from_url("https://www.amazon.com/dp/B07FTKQ97Q") == "B07FTKQ97Q"
    assert extract_asin_from_url("B08N5WRWNW") == "B08N5WRWNW"
    assert extract_asin_from_url("https://example.com/product/123") is None


def test_extract_walmart_product_id_from_url_and_direct_value():
    assert (
        extract_product_id_from_walmart_url("https://www.walmart.com/ip/Test-Item/123456789")
        == "123456789"
    )
    assert extract_product_id_from_walmart_url("987654321") == "987654321"
    assert extract_product_id_from_walmart_url("https://example.com/item/abc") is None


def test_truncate_text():
    assert truncate_text("abcdef", max_length=3) == "abc..."
    assert truncate_text("abc", max_length=5) == "abc"


def test_detect_review_column_returns_first_match():
    df = pd.DataFrame({"title": ["x"], "review": ["good"], "body": ["ok"]})
    col = detect_review_column(df, ["review_text", "review", "body"])
    assert col == "review"


def test_format_helpers():
    assert format_confidence(0.853) == "85.3%"
    assert format_confidence(None) == "N/A"
    assert format_metric(0.123456, 3) == "0.123"
    assert format_metric("N/A") == "N/A"
