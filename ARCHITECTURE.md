# Fake Review Detector - Modular Architecture

A professional, production-ready Streamlit application for detecting fake reviews using ensemble machine learning models. This refactored version follows Python and Streamlit best practices with a clean, modular architecture.

## 📁 Project Structure

```
fake-review-detector/
│
├── main_modular.py              # Main entry point (clean & minimal)
│
├── config.py                     # Configuration & constants
├── utils.py                      # Utility functions (text processing, extraction)
├── model_handler.py              # Model loading and management
├── predictor.py                  # Prediction logic and ensemble voting
├── scraper.py                    # API integrations (Amazon, Walmart)
│
├── ui/                           # UI Components
│   ├── __init__.py
│   └── components.py             # Display functions (tables, charts)
│
├── pages/                        # Page modules
│   ├── __init__.py
│   ├── single_review.py          # Single review analysis
│   ├── csv_batch.py              # CSV batch analysis
│   ├── amazon_product.py         # Amazon product analysis
│   └── walmart_product.py        # Walmart product analysis
│
├── models/                       # Trained models directory
│   └── *.pkl                     # Pickle files of trained models
│
├── dataset/                      # Data directory
│   ├── train.csv
│   └── test.csv
│
└── requirements.txt              # Python dependencies
```

## 🗂️ Module Description

### Core Modules

#### `main_modular.py` (Entry Point)
- Clean, minimal Streamlit app entry point
- Handles page initialization, resource loading, and tab navigation
- ~120 lines (vs 1700+ in original)

```python
if __name__ == "__main__":
    main()
```

#### `config.py` (Configuration)
- Centralized constants and configuration
- Environment paths, API keys, color schemes
- UI messages and labels
- Easy to maintain and update

```python
MODELS_DIR = "models"
AMAZON_API_URL = "https://api.scraperapi.com/structured/amazon/product/v1"
COLORS = {"genuine": "#2ecc71", "fake": "#e74c3c", ...}
```

#### `utils.py` (Utilities)
- Text cleaning and preprocessing
- URL extraction (ASIN, Walmart Product ID)
- Text truncation and formatting
- CSV column detection

```python
def clean_text(text: str) -> str: ...
def extract_asin_from_url(url: str) -> Optional[str]: ...
```

#### `model_handler.py` (Model Management)
- Load available models from directory
- Load model performance metrics
- Cached using @st.cache_resource for performance

```python
@st.cache_resource
def load_available_models() -> Dict[str, Any]: ...
```

#### `predictor.py` (Prediction Logic)
- Predict review authenticity
- Calculate confidence scores
- Ensemble voting logic
- Determine trust levels

```python
def predict_review(text, models, ensemble=True) -> Tuple[int, float, ...]: ...
```

#### `scraper.py` (API Integration)
- Fetch Amazon product reviews
- Fetch Walmart product reviews
- Error handling and timeout management

```python
def fetch_amazon_reviews(asin: str) -> Optional[Dict]: ...
```

### UI Components

#### `ui/components.py`
- Display metrics in table format
- Generate interactive charts (Plotly)
- Display summary metrics and distributions

```python
def display_metrics_table(...): ...
def display_review_metrics_charts(...): ...
def display_summary_metrics(...): ...
```

### Page Modules

#### `pages/single_review.py`
- Single review analysis interface
- Individual model predictions
- Visual analytics per review

#### `pages/csv_batch.py`
- CSV file upload and processing
- Batch analysis with progress tracking
- Results filtering and download

#### `pages/amazon_product.py`
- Amazon product URL/ASIN input
- Multi-review analysis
- Product information display

#### `pages/walmart_product.py`
- Walmart product URL/ID input
- Verified purchase detection
- Incentivized review flagging

## 🚀 Usage

### Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the modular version
streamlit run main_modular.py
```

### Project Structure Benefits

1. **Modularity**: Each responsibility has its own module
2. **Reusability**: Functions can be imported and reused
3. **Testability**: Easy to write unit tests for each module
4. **Maintainability**: Clear separation of concerns
5. **Scalability**: Easy to add new features or pages
6. **Performance**: Caching and optimization built-in

## 📝 Key Architecture Patterns

### 1. Configuration Management
All constants in `config.py` instead of scattered throughout code:
```python
from config import MODELS_DIR, COLORS, API_TIMEOUT
```

### 2. Utility Functions
Reusable helper functions in `utils.py`:
```python
from utils import clean_text, extract_asin_from_url, truncate_text
```

### 3. Separation of Concerns
- Business logic in `predictor.py`
- API calls in `scraper.py`
- UI in `pages/` and `ui/`
- Configuration in `config.py`

### 4. Type Hints
All functions have proper type annotations:
```python
def show_single_review_page(
    models: Dict[str, Any],
    metrics: Dict,
    use_ensemble: bool,
    selected_model: str,
) -> None:
```

### 5. Documentation
- Module docstrings
- Function docstrings with Args/Returns
- Inline comments for complex logic

## 📊 Size Comparison

| Metric          | Original  | Modular                 |
| --------------- | --------- | ----------------------- |
| Lines in main   | 1700+     | 120                     |
| Total lines     | ~1700     | ~2000 (across 10 files) |
| Maintainability | Low       | High                    |
| Reusability     | Low       | High                    |
| Test Coverage   | Difficult | Easy                    |

## 🔄 Migration Guide

To use the modular version:

1. Replace `main.py` import with `main_modular.py`
2. All functionality is preserved
3. Configuration can be easily updated in `config.py`
4. New features can be added as new page modules

## 📚 Adding New Features

### To Add a New Page:

1. Create `pages/new_feature.py`
2. Define `show_new_feature_page()` function
3. Import in `main_modular.py`
4. Add tab for new page

### To Add New Models:

1. Place `.pkl` files in `models/` directory
2. Models auto-load in `model_handler.py`
3. No code changes needed!

## 🛠️ Development Standards

### Code Style
- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Keep functions focused (single responsibility)

### Import Organization
```python
# Standard library
import os
import re

# Third-party
import streamlit as st
import pandas as pd

# Local
from config import MODELS_DIR
from utils import clean_text
```

### File Naming
- Modules: `snake_case.py`
- Functions: `snake_case()`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`

## 📦 Dependencies

See `requirements.txt` for all dependencies. Key packages:
- `streamlit`: Web framework
- `scikit-learn`: ML models
- `pandas`: Data processing
- `plotly`: Interactive charts
- `nltk`: Text processing

## 🚧 Future Improvements

- Unit tests for each module
- Logger implementation
- Database integration
- API endpoint for predictions
- Model version management
- User feedback storage
- Advanced analytics dashboard

## 📄 License

MIT License

## 👥 Contributing

1. Follow the modular structure
2. Add type hints to functions
3. Document your code
4. Write unit tests
5. Submit pull requests

---

**This modular architecture makes the codebase professional, maintainable, and scalable!**
