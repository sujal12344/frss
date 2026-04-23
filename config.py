"""
Configuration and constants for the Fake Review Detection application.
"""

import os

# ==================== APPLICATION SETTINGS ====================

# Page configuration
PAGE_CONFIG = {
    "page_title": "Fake Review Detection",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# ==================== DIRECTORIES ====================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
CACHE_DIR = os.path.join(BASE_DIR, "cache_dir")
DATA_DIR = os.path.join(BASE_DIR, "dataset")

# ==================== API KEYS ====================

SCRAPER_API_KEY = "2e3a0b27898501a44e5f18eff3e1775d"

# ==================== API ENDPOINTS ====================

AMAZON_API_URL = "https://api.scraperapi.com/structured/amazon/product/v1"
WALMART_API_URL = "https://api.scraperapi.com/structured/walmart/review/v1"
API_TIMEOUT = 60

# ==================== PREDICTION SETTINGS ====================

CONFIDENCE_THRESHOLD = 0.5
MIN_TEXT_LENGTH = 10

# ==================== UI MESSAGES ====================

MESSAGES = {
    "no_models_found": "❌ No models found! Please train models first using `train_model_1M.ipynb`",
    "models_loaded": "✅ Loaded {count} models: {models}",
    "invalid_review": "⚠️ Please enter a review text!",
    "analyzing": "🔄 Analyzing review...",
    "no_text": "❌ Could not analyze the review!",
    "no_reviews_found": "⚠️ No reviews found for this product!",
    "csv_format_error": "❌ Error processing CSV: {error}",
    "csv_hint": "💡 Make sure your CSV has a column with review text.",
}

# ==================== UI LABELS ====================

POSSIBLE_REVIEW_COLUMNS = [
    "review_text",
    "review",
    "text",
    "text_",
    "Review",
    "comment",
    "Comment",
    "body",
    "Body",
    "content",
    "Content",
]

# ==================== PREDICTION OUTCOMES ====================

PREDICTIONS = {
    0: {"label": "❌ FAKE", "color": "error", "full_label": "Fake"},
    1: {"label": "✅ GENUINE", "color": "success", "full_label": "Genuine"},
}

# ==================== TRUST LEVELS ====================

TRUST_LEVELS = {
    "genuine": {"threshold": 95, "label": "Genuine Reviews"},
    "authentic": {"threshold": 90, "label": "Authentic Reviews"},
    "mostly_genuine": {"threshold": 85, "label": "Mostly Genuine Reviews"},
    "largely_genuine": {"threshold": 80, "label": "Largely Genuine Reviews"},
    "generally_genuine": {"threshold": 75, "label": "Generally Genuine Reviews"},
    "balanced": {"threshold": 65, "label": "Balanced Reviews"},
    "mixed": {"threshold": 55, "label": "Mixed Reviews"},
    "some_fake": {"threshold": 45, "label": "Some Fake Reviews Detected"},
    "many_fake": {"threshold": 35, "label": "Many Fake Reviews Detected"},
    "high_fake": {"threshold": 25, "label": "High Fake Review Presence"},
    "mostly_fake": {"threshold": 15, "label": "Mostly Fake Reviews"},
    "fake_dominated": {"threshold": 0, "label": "Fake Reviews Dominated"},
}

# ==================== COLORS ====================

COLORS = {
    "genuine": "#2ecc71",
    "fake": "#e74c3c",
    "confidence": "#3498db",
    "accuracy": "#2ecc71",
    "precision": "#f39c12",
    "recall": "#9b59b6",
    "f1_score": "#e74c3c",
    "time": "#e67e22",
}

# ==================== CHART SETTINGS ====================

CHART_HEIGHT = 350
CHART_TIME_HEIGHT = 300
CHART_HOVERMODE = "x unified"
