"""
Fake Review Detection - Main Application Entry Point
Streamlit app for detecting fake reviews using ensemble ML models.
"""

from typing import Any, Dict

import streamlit as st

from config import MESSAGES, PAGE_CONFIG
from model_handler import load_available_models, load_model_metrics
from pages.amazon_product import show_amazon_product_page
from pages.csv_batch import show_csv_batch_page
from pages.single_review import show_single_review_page
from pages.walmart_product import show_walmart_product_page

PAGE_ROUTES = {
    "home": "Home",
    "single-review": "Single Review",
    "amazon-product": "Amazon Product Review",
    "csv-batch": "CSV Batch",
    "walmart-review": "Walmart Product Review",
}


def initialize_app() -> None:
    """Initialize Streamlit page configuration."""
    st.set_page_config(
        page_title=PAGE_CONFIG["page_title"],
        layout=PAGE_CONFIG["layout"] or "wide",  # type: ignore
        initial_sidebar_state="collapsed",
    )


def apply_global_styles(dark_mode: bool = False) -> None:
    """Apply premium light/dark styling across the app."""
    theme_vars = (
        """
                --bg: #0b1220;
                --bg-soft: #121c2f;
                --fg: #e8eef7;
                --muted: #a8b4c9;
                --title: #f8fbff;
                --primary: #2ec4b6;
                --primary-glow: #6ce5da;
                --card: rgba(20, 30, 48, 0.78);
                --border: rgba(173, 196, 230, 0.24);
                --shadow: 0 14px 36px -14px rgba(3, 8, 19, 0.8);
        """
        if dark_mode
        else """
                --bg: #f5f8fc;
                --bg-soft: #eaf0f7;
                --fg: #0f1b22;
                --muted: #5b6b75;
                --title: #060a14;
                --primary: #0aa5a1;
                --primary-glow: #34d4c8;
                --card: rgba(255, 255, 255, 0.86);
                --border: #d6e0ea;
                --shadow: 0 14px 36px -16px rgba(16, 36, 64, 0.22);
        """
    )

    st.markdown(
        """
        <style>
            :root {
__THEME_VARS__
            }

            html,
            body,
            .stApp {
                background:
                    radial-gradient(1200px 500px at -10% -10%, rgba(52, 212, 200, 0.20), transparent 60%),
                    radial-gradient(900px 400px at 110% -10%, rgba(65, 120, 255, 0.16), transparent 62%),
                    linear-gradient(180deg, var(--bg) 0%, var(--bg-soft) 100%) !important;
                color: var(--fg) !important;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }

            #MainMenu,
            footer,
            header[data-testid="stHeader"],
            div[data-testid="stToolbar"],
            section[data-testid="stSidebarNav"],
            div[data-testid="stSidebarNav"],
            nav[aria-label="Pages"] {
                display: none !important;
            }

            .block-container {
                padding-top: 1.5rem;
                max-width: 1200px;
            }

            .theme-toggle-wrap {
                margin-bottom: 0.35rem;
            }

            /* ===== DARK MODE TOGGLE STYLING ===== */
            .theme-toggle-wrap {
                display: flex;
                justify-content: flex-end;
                align-items: center;
                margin-bottom: 0.35rem;
            }

            .theme-toggle-wrap [data-testid="stToggle"] {
                background: linear-gradient(135deg, var(--card) 0%, rgba(255,255,255,0.08) 100%);
                border: 1.5px solid var(--border);
                border-radius: 999px;
                padding: 0.3rem 1rem 0.35rem;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255,255,255,0.2);
                backdrop-filter: blur(12px);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }

            .theme-toggle-wrap [data-testid="stToggle"]:hover {
                border-color: var(--primary);
                box-shadow: 0 12px 32px rgba(10, 165, 161, 0.15), inset 0 1px 0 rgba(255,255,255,0.3);
                transform: translateY(-2px);
            }

            .theme-toggle-wrap [data-testid="stToggle"] label {
                font-size: 0.9rem;
                font-weight: 600;
                color: var(--fg);
                margin: 0;
                letter-spacing: 0.3px;
            }

            .theme-toggle-wrap [data-testid="stToggle"] span {
                color: var(--fg) !important;
            }

            /* ===== LIGHT MODE SPECIFIC: Make toggle text visible ===== */
            .stApp[data-theme="light"] .theme-toggle-wrap [data-testid="stToggle"] label,
            .stApp[data-theme="light"] .theme-toggle-wrap [data-testid="stToggle"] span {
                color: #0f1b22 !important;
            }

            .app-title {
                font-size: clamp(3.4rem, 6.5vw, 4.8rem);
                line-height: 1.05;
                font-weight: 950;
                color: var(--title);
                margin: -0.35rem auto 1.2rem;
                letter-spacing: -0.025em;
                text-align: center;
                background: linear-gradient(135deg, var(--title) 0%, var(--primary) 75%, var(--primary-glow) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                display: block;
                text-shadow: 0 2px 10px rgba(10, 165, 161, 0.1);
            }

            .nav {
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 0.85rem 1.2rem;
                border: 1.5px solid var(--border);
                border-radius: 16px;
                background: linear-gradient(135deg, var(--card) 0%, rgba(255,255,255,0.05) 100%);
                backdrop-filter: blur(10px);
                margin-bottom: 2rem;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08), inset 0 1px 0 rgba(255,255,255,0.15);
                transition: all 0.3s ease;
            }

            .nav:hover {
                border-color: var(--primary);
                box-shadow: 0 16px 48px rgba(10, 165, 161, 0.12), inset 0 1px 0 rgba(255,255,255,0.2);
            }

            .nav .links {
                display: flex;
                gap: 0.6rem;
                flex-wrap: wrap;
                width: 100%;
                justify-content: center;
            }

            .nav .links a {
                margin-left: 0;
                color: var(--muted);
                text-decoration: none;
                font-size: 0.95rem;
                font-weight: 650;
                padding: 0.55rem 1.1rem;
                border-radius: 999px;
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
                letter-spacing: 0.2px;
            }

            .nav .links a.active {
                color: #ffffff;
                background: linear-gradient(135deg, var(--primary) 0%, var(--primary-glow) 100%);
                box-shadow: 0 8px 24px rgba(10, 165, 161, 0.3);
                transform: translateY(-2px);
            }

            .nav .links a:hover {
                color: var(--primary);
                background: rgba(10, 165, 161, 0.12);
                transform: translateY(-1px);
            }

            .hero {
                text-align: center;
                padding: 4rem 2rem 3rem;
                background: linear-gradient(135deg, 
                    rgba(10, 165, 161, 0.08) 0%, 
                    transparent 50%,
                    rgba(52, 212, 200, 0.06) 100%);
                border-radius: 24px;
                border: 1.5px solid var(--border);
                box-shadow: 0 16px 48px rgba(0, 0, 0, 0.12), inset 0 1px 1px rgba(255,255,255,0.1);
                backdrop-filter: blur(8px);
                transition: all 0.3s ease;
            }

            .hero:hover {
                border-color: var(--primary);
                box-shadow: 0 20px 56px rgba(10, 165, 161, 0.15), inset 0 1px 1px rgba(255,255,255,0.15);
            }

            .hero .badge {
                display: inline-block;
                padding: 0.45rem 1rem;
                border-radius: 999px;
                background: linear-gradient(135deg, rgba(10, 165, 161, 0.15), rgba(52, 212, 200, 0.08));
                color: var(--primary);
                font-size: 0.82rem;
                font-weight: 700;
                letter-spacing: 0.5px;
                margin-bottom: 1.25rem;
                border: 1px solid rgba(10, 165, 161, 0.3);
                box-shadow: 0 4px 12px rgba(10, 165, 161, 0.15);
            }

            .hero h1 {
                font-size: clamp(1.8rem, 4vw, 2.8rem);
                line-height: 1.15;
                font-weight: 900;
                margin: 0 0 1.2rem;
                color: var(--fg);
                letter-spacing: -0.01em;
            }

            .hero h1 .grad {
                background: linear-gradient(90deg, var(--primary), var(--primary-glow));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .hero p {
                color: var(--muted);
                max-width: 700px;
                margin: 0 auto;
                font-size: 1.08rem;
                line-height: 1.7;
                font-weight: 500;
            }

            .frs-stats {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1.25rem;
                margin: 2.5rem 0;
            }

            @media (max-width: 768px) {
                .frs-stats {
                    grid-template-columns: repeat(1, 1fr);
                    gap: 1rem;
                }
            }

            .frs-stat {
                background: linear-gradient(135deg, var(--card) 0%, rgba(255,255,255,0.04) 100%);
                border: 1.5px solid var(--border);
                border-radius: 18px;
                padding: 1.5rem 1.25rem;
                text-align: center;
                box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08), inset 0 1px 1px rgba(255,255,255,0.1);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                backdrop-filter: blur(4px);
            }

            .frs-stat:hover {
                transform: translateY(-6px);
                border-color: var(--primary);
                box-shadow: 0 16px 48px rgba(10, 165, 161, 0.2), inset 0 1px 1px rgba(255,255,255,0.15);
            }

            .frs-stat .value {
                font-size: 2rem;
                font-weight: 900;
                background: linear-gradient(135deg, var(--primary), var(--primary-glow));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.35rem;
                letter-spacing: -0.01em;
            }

            .frs-stat .label {
                color: var(--muted);
                font-size: 0.88rem;
                font-weight: 600;
                letter-spacing: 0.3px;
            }

            .frs-section-title {
                text-align: center;
                font-size: 2rem;
                font-weight: 900;
                margin: 3rem 0 0.75rem;
                color: var(--fg);
                letter-spacing: -0.015em;
                background: linear-gradient(90deg, var(--fg) 0%, var(--primary) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .frs-section-sub {
                text-align: center;
                color: var(--muted);
                margin-bottom: 2rem;
                font-size: 1.05rem;
                font-weight: 500;
                letter-spacing: 0.2px;
            }

            .frs-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 1rem;
            }

            @media (max-width: 900px) {
                .frs-grid {
                    grid-template-columns: 1fr;
                }
            }

            .frs-card {
                background: linear-gradient(135deg, var(--card) 0%, rgba(255,255,255,0.05) 100%);
                border: 1.5px solid var(--border);
                border-radius: 18px;
                padding: 1.75rem;
                height: 100%;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08), inset 0 1px 1px rgba(255,255,255,0.1);
                backdrop-filter: blur(4px);
            }

            .frs-card:hover {
                transform: translateY(-8px) scaleX(1.01);
                box-shadow: 0 24px 56px rgba(10, 165, 161, 0.25), inset 0 1px 1px rgba(255,255,255,0.15);
                border-color: var(--primary);
            }

            .frs-card .badge {
                width: 56px;
                height: 56px;
                border-radius: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.75rem;
                margin-bottom: 1.2rem;
                background: linear-gradient(135deg, var(--primary), var(--primary-glow));
                color: #fff;
                box-shadow: 0 8px 24px rgba(10, 165, 161, 0.3);
                transition: all 0.3s ease;
            }

            .frs-card:hover .badge {
                transform: scale(1.1) rotate(6deg);
                box-shadow: 0 12px 32px rgba(10, 165, 161, 0.4);
            }

            .frs-card h3 {
                margin: 0 0 0.5rem;
                color: var(--fg);
                font-size: 1.22rem;
                font-weight: 800;
                letter-spacing: -0.005em;
            }

            .frs-card p {
                color: var(--muted);
                font-size: 0.95rem;
                margin: 0;
                line-height: 1.6;
                font-weight: 500;
            }

            .frs-footer {
                text-align: center;
                color: var(--muted);
                font-size: 0.88rem;
                padding: 2.5rem 0 1.5rem;
                border-top: 1.5px solid var(--border);
                margin-top: 4rem;
                font-weight: 500;
                letter-spacing: 0.3px;
            }

            section[data-testid="stSidebar"] > div {
                background: var(--card);
                border-right: 1px solid var(--border);
                padding-top: 0.65rem;
            }

            section[data-testid="stSidebar"] .block-container {
                padding-top: 0.35rem;
            }

        </style>
        """.replace(
            "__THEME_VARS__", theme_vars
        ),
        unsafe_allow_html=True,
    )

    if dark_mode:
        st.markdown(
            """
            <style>
                div[data-testid="stToggle"],
                div[data-testid="stToggle"] * {
                    color: #ffffff !important;
                }

                div[data-testid="stWidgetLabel"],
                div[data-testid="stWidgetLabel"] label,
                label[data-testid="stWidgetLabel"],
                section[data-testid="stSidebar"] * {
                    color: #ffffff !important;
                }

                section[data-testid="stSidebar"] .stCheckbox label,
                section[data-testid="stSidebar"] .stSelectbox label,
                section[data-testid="stSidebar"] .stTextInput label,
                section[data-testid="stSidebar"] .stTextArea label,
                section[data-testid="stSidebar"] .stMarkdown,
                section[data-testid="stSidebar"] .stCaption,
                section[data-testid="stSidebar"] .stInfo,
                section[data-testid="stSidebar"] .stInfo * {
                    color: #ffffff !important;
                }

                section[data-testid="stSidebar"] div[data-baseweb="select"],
                section[data-testid="stSidebar"] div[data-baseweb="select"] * {
                    color: #000000 !important;
                }

                textarea,
                input,
                div[data-baseweb="select"] input,
                div[data-baseweb="select"] [role="combobox"] {
                    color: #000000 !important;
                }

                textarea::placeholder,
                input::placeholder {
                    color: rgba(0, 0, 0, 0.5) !important;
                }

                div[data-testid="stTextArea"] label,
                div[data-testid="stTextInput"] label {
                    color: #ffffff !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
                /* ===== ABSOLUTE LIGHT MODE OVERRIDES ===== */
                
                /* Container level */
                .theme-toggle-wrap {
                    color: #0f1b22 !important;
                }
                
                /* All text inside toggle */
                .theme-toggle-wrap,
                .theme-toggle-wrap *,
                .theme-toggle-wrap div,
                .theme-toggle-wrap label,
                .theme-toggle-wrap span {
                    color: #0f1b22 !important;
                    fill: #0f1b22 !important;
                }
                
                /* Toggle specific overrides */
                .theme-toggle-wrap [data-testid="stToggle"],
                div[data-testid="stToggle"] {
                    background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(245,248,252,0.95) 100%) !important;
                    border: 1.5px solid #d6e0ea !important;
                }

                .theme-toggle-wrap [data-testid="stToggle"] label,
                div[data-testid="stToggle"] label,
                [data-testid="stToggle"] label {
                    color: #0f1b22 !important;
                    font-weight: 900 !important;
                    visibility: visible !important;
                    opacity: 1 !important;
                }

                .theme-toggle-wrap [data-testid="stToggle"] span,
                div[data-testid="stToggle"] span,
                [data-testid="stToggle"] span {
                    color: #0f1b22 !important;
                    font-weight: 800 !important;
                    visibility: visible !important;
                    opacity: 1 !important;
                }
                
                /* Widget labels */
                div[data-testid="stWidgetLabel"],
                div[data-testid="stWidgetLabel"] label,
                div[data-testid="stWidgetLabel"] span,
                label[data-testid="stWidgetLabel"] {
                    color: #0f1b22 !important;
                    font-weight: 600 !important;
                }

                /* Input elements styling */
                textarea,
                input,
                div[data-baseweb="select"] input,
                div[data-baseweb="select"] [role="combobox"] {
                    background: #ffffff !important;
                    color: #0f1b22 !important;
                    border-color: #d6e0ea !important;
                }

                textarea::placeholder,
                input::placeholder {
                    color: rgba(91, 107, 117, 0.8) !important;
                }

                /* Sidebar text colors - ensure visible */
                section[data-testid="stSidebar"] label,
                section[data-testid="stSidebar"] span,
                section[data-testid="stSidebar"] .stMarkdown,
                section[data-testid="stSidebar"] .stCaption,
                section[data-testid="stSidebar"] .stInfo,
                section[data-testid="stSidebar"] .stCheckbox label,
                section[data-testid="stSidebar"] .stSelectbox label {
                    color: #0f1b22 !important;
                    visibility: visible !important;
                    opacity: 1 !important;
                }

                div[data-testid="stTextArea"] label,
                div[data-testid="stTextInput"] label,
                .stTextArea label,
                .stTextInput label {
                    color: #0f1b22 !important;
                    font-weight: 600 !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )


def get_active_page() -> str:
    """Return the current page from query params."""
    page = st.query_params.get("page", "home")
    if isinstance(page, list):
        page = page[0] if page else "home"

    return page if page in PAGE_ROUTES else "home"


def get_active_theme() -> bool:
    """Return dark mode state from session state without reinitializing."""
    # Only read, never reinitialize - let render_theme_toggle handle that
    return st.session_state.get("ui_dark_mode", False)


def render_theme_toggle() -> bool:
    """Render theme toggle at top-right and return current dark mode state."""
    # Initialize session state if not already set
    if "ui_dark_mode" not in st.session_state:
        st.session_state["ui_dark_mode"] = False  # Default: light mode

    _, right_col = st.columns([0.82, 0.18])
    with right_col:
        st.markdown("<div class='theme-toggle-wrap'>", unsafe_allow_html=True)
        # Toggle uses session_state directly - persists across page changes
        dark_mode = st.toggle(
            "Dark Mode", value=st.session_state["ui_dark_mode"], key="ui_dark_mode"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    return bool(dark_mode)


def _build_page_href(page_key: str) -> str:
    # Only use page param - theme is managed by session_state
    return f"?page={page_key}"


def render_navbar(active_page: str, dark_mode: bool) -> None:
    """Render the top navigation bar."""
    nav_items = []
    for page_key, label in PAGE_ROUTES.items():
        href = _build_page_href(page_key)
        active_class = "active" if page_key == active_page else ""
        nav_items.append(
            f'<a class="{active_class}" href="{href}" target="_self">{label}</a>'
        )

    st.markdown(
        f"""
        <h1 class="app-title">Fake Review Detector</h1>
        <div class="nav">
            <div class="links">
                {''.join(nav_items)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home_page() -> None:
    """Render the application landing page."""
    st.markdown(
        """
        <div class="hero">
            <div class="badge">✦ FAKE REVIEW INTELLIGENCE</div>
            <h1>
                Reliable review analysis for smarter choices.
            </h1>
            <p>
                Protect your business and customers from deceptive reviews.
                Analyze single reviews, batch CSV files, or scrape directly from
                Amazon and Walmart with our state-of-the-art AI detection system.
            </p>
        </div>

        <div class="frs-stats">
            <div class="frs-stat">
                <div class="value">1M+</div>
                <div class="label">Reviews Analyzed</div>
            </div>
            <div class="frs-stat">
                <div class="value">4</div>
                <div class="label">Detection Modes</div>
            </div>
            <div class="frs-stat">
                <div class="value">&lt;2s</div>
                <div class="label">Avg Response Time</div>
            </div>
        </div>

        <div class="frs-section-sub">Four powerful ways to identify fake reviews</div>

        <div class="frs-grid">
            <div class="frs-card">
                <div class="badge">📝</div>
                <h3>Single Review</h3>
                <p>Paste any review text and get instant analysis with confidence scoring.</p>
            </div>
            <div class="frs-card">
                <div class="badge">📊</div>
                <h3>CSV Batch</h3>
                <p>Upload a CSV file with multiple reviews and analyze them all at once.</p>
            </div>
            <div class="frs-card">
                <div class="badge">🛒</div>
                <h3>Amazon Product Review</h3>
                <p>Enter an Amazon product URL and analyze its reviews.</p>
            </div>
            <div class="frs-card">
                <div class="badge">🏬</div>
                <h3>Walmart Product Review</h3>
                <p>Analyze reviews directly from any Walmart product page.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_home() -> None:
    """Show guidance content in the sidebar on the landing page."""
    st.sidebar.markdown("### Quick Start")
    st.sidebar.markdown(
        """
        1. Open **Single Review** for one comment.
        2. Use **CSV Batch** for bulk analysis.
        3. Try **Amazon** or **Walmart** pages for product reviews.
        """
    )
    st.sidebar.markdown("---")
    st.sidebar.info(
        "Upload or paste review text, then compare ensemble predictions and confidence."
    )
    st.sidebar.markdown("---")
    st.sidebar.caption(
        "Designed for fast fake-review screening across multiple sources."
    )


def load_resources() -> tuple:
    """
    Load all required resources (models and metrics).

    Returns:
        Tuple of (models_dict, metrics_dict)
    """
    models = load_available_models()
    metrics = load_model_metrics()

    if not models:
        st.error(
            "❌ No models found! Please train models first using `train_model_1M.ipynb`"
        )
        st.stop()

    return models, metrics


def setup_sidebar(models: dict) -> tuple:
    """
    Setup sidebar settings and options.

    Args:
        models: Dictionary of loaded models

    Returns:
        Tuple of (use_ensemble, selected_model, show_model_details)
    """
    st.sidebar.header("⚙️ Settings")

    use_ensemble = st.sidebar.checkbox(
        "🤖 Use Ensemble (Majority Vote)", value=True, key="ensemble_checkbox"
    )
    selected_model = st.sidebar.selectbox(
        "📊 Single Model (if not ensemble)",
        list(models.keys()),
        key="model_selectbox",
    )
    show_model_details = st.sidebar.checkbox(
        "📈 Show Model Performance", value=False, key="model_details_checkbox"
    )

    st.sidebar.markdown("---")
    st.sidebar.info(
        "💡 **Tip:** Ensemble mode combines multiple models for better accuracy!"
    )

    return use_ensemble, selected_model, show_model_details


def display_model_metrics_sidebar(models: dict, metrics: dict, show: bool) -> None:
    """
    Display model metrics in sidebar if enabled.

    Args:
        models: Dictionary of loaded models
        metrics: Model metrics dictionary
        show: Whether to display metrics
    """
    if not show or not metrics:
        return

    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Model Metrics")

    # Sort models by accuracy in descending order
    sorted_models = sorted(
        [(name, metrics[name]) for name in models.keys() if name in metrics],
        key=lambda x: x[1].get("accuracy", 0),
        reverse=True,
    )

    for model_name, m in sorted_models:
        st.sidebar.write(f"**{model_name}**")
        st.sidebar.write(f"- Accuracy: {m.get('accuracy', 'N/A')}")
        st.sidebar.write(f"- Precision: {m.get('precision', 'N/A')}")
        st.sidebar.write(f"- F1-Score: {m.get('f1_score', 'N/A')}")


def show_tabs(
    models: dict,
    metrics: dict,
    use_ensemble: bool,
    selected_model: str,
) -> None:
    """
    Display and handle tab navigation.

    Args:
        models: Dictionary of loaded models
        metrics: Model metrics dictionary
        use_ensemble: Whether to use ensemble voting
        selected_model: Selected single model name
    """
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "✍️ Single Review Analysis",
            "📤 CSV Batch Analysis",
            "🔗 Amazon Product Analysis",
            "🛒 Walmart Product Analysis",
        ]
    )

    with tab1:
        show_single_review_page(models, metrics, use_ensemble, selected_model)

    with tab2:
        show_csv_batch_page(models, metrics, use_ensemble)

    with tab3:
        show_amazon_product_page(models, metrics, use_ensemble)

    with tab4:
        show_walmart_product_page(models, metrics, use_ensemble)


def show_footer() -> None:
    """Display application footer."""
    st.markdown(
        """
    <div class="frs-footer">
        © 2025 Fake Review Detector · Built with Streamlit
    </div>
    """,
        unsafe_allow_html=True,
    )


def main() -> None:
    """Main application entry point."""
    initialize_app()
    dark_mode = render_theme_toggle()
    apply_global_styles(dark_mode)

    current_page = get_active_page()
    render_navbar(current_page, dark_mode)

    if current_page == "home":
        render_sidebar_home()
        render_home_page()
        return

    models, metrics = load_resources()
    use_ensemble, selected_model, show_model_details = setup_sidebar(models)
    display_model_metrics_sidebar(models, metrics, show_model_details)

    if current_page == "single-review":
        show_single_review_page(models, metrics, use_ensemble, selected_model)
    elif current_page == "csv-batch":
        show_csv_batch_page(models, metrics, use_ensemble)
    elif current_page == "amazon-product":
        show_amazon_product_page(models, metrics, use_ensemble)
    elif current_page == "walmart-review":
        show_walmart_product_page(models, metrics, use_ensemble)
    else:
        render_home_page()

    show_footer()


if __name__ == "__main__":
    main()
