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

            [data-testid="stToggle"] {
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 999px;
                padding: 0.15rem 0.65rem 0.2rem;
                box-shadow: var(--shadow);
            }

            .app-title {
                font-size: clamp(3.2rem, 6vw, 4.6rem);
                line-height: 1.1;
                font-weight: 900;
                color: var(--title);
                margin: -0.25rem auto 1rem;
                letter-spacing: -0.02em;
                text-align: center;
                background: linear-gradient(135deg, var(--title) 0%, var(--primary) 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                display: block;
            }

            .nav {
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 0.7rem 1rem;
                border: 1px solid var(--border);
                border-radius: 14px;
                background: var(--card);
                backdrop-filter: blur(8px);
                margin-bottom: 1.5rem;
                box-shadow: var(--shadow);
            }

            .nav .links {
                display: flex;
                gap: 0.5rem;
                flex-wrap: wrap;
                width: 100%;
                justify-content: center;
            }

            .nav .links a {
                margin-left: 0;
                color: var(--muted);
                text-decoration: none;
                font-size: 0.92rem;
                font-weight: 600;
                padding: 0.48rem 0.9rem;
                border-radius: 999px;
                transition: all 0.18s ease;
            }

            .nav .links a.active {
                color: #ffffff;
                background: linear-gradient(135deg, var(--primary), var(--primary-glow));
            }

            .nav .links a:hover {
                color: var(--primary);
                background: rgba(10, 165, 161, 0.08);
            }

            .hero {
                text-align: center;
                padding: 3rem 1rem 2rem;
                background: radial-gradient(1200px 400px at 50% 0%, rgba(10, 165, 161, 0.10), transparent 60%);
                border-radius: 20px;
                border: 1px solid var(--border);
                box-shadow: var(--shadow);
            }

            .hero .badge {
                display: inline-block;
                padding: 0.35rem 0.85rem;
                border-radius: 999px;
                background: rgba(10, 165, 161, 0.10);
                color: var(--primary);
                font-size: 0.8rem;
                font-weight: 600;
                margin-bottom: 1rem;
            }

            .hero h1 {
                font-size: clamp(1.7rem, 3.8vw, 2.6rem);
                line-height: 1.1;
                font-weight: 800;
                margin: 0 0 1rem;
                color: var(--fg);
            }

            .hero h1 .grad {
                background: linear-gradient(90deg, var(--primary), var(--primary-glow));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .hero p {
                color: var(--muted);
                max-width: 680px;
                margin: 0 auto;
                font-size: 1.05rem;
                line-height: 1.6;
            }

            .frs-stats {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1rem;
                margin: 2rem 0;
            }

            @media (max-width: 768px) {
                .frs-stats {
                    grid-template-columns: repeat(1, 1fr);
                }
            }

            .frs-stat {
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 14px;
                padding: 1.25rem;
                text-align: center;
                box-shadow: var(--shadow);
            }

            .frs-stat .value {
                font-size: 1.8rem;
                font-weight: 800;
                color: var(--primary);
                margin-bottom: 0.25rem;
            }

            .frs-stat .label {
                color: var(--muted);
                font-size: 0.85rem;
            }

            .frs-section-title {
                text-align: center;
                font-size: 1.8rem;
                font-weight: 700;
                margin: 2.5rem 0 0.5rem;
                color: var(--fg);
            }

            .frs-section-sub {
                text-align: center;
                color: var(--muted);
                margin-bottom: 1.75rem;
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
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 1.5rem;
                height: 100%;
                transition: transform .2s ease, box-shadow .2s ease;
                box-shadow: var(--shadow);
            }

            .frs-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 18px 40px -18px rgba(10, 165, 161, 0.30);
                border-color: var(--primary);
            }

            .frs-card .badge {
                width: 48px;
                height: 48px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                margin-bottom: 1rem;
                background: linear-gradient(135deg, var(--primary), var(--primary-glow));
                color: #fff;
            }

            .frs-card h3 {
                margin: 0 0 .35rem;
                color: var(--fg);
                font-size: 1.15rem;
            }

            .frs-card p {
                color: var(--muted);
                font-size: 0.92rem;
                margin: 0;
            }

            .frs-footer {
                text-align: center;
                color: var(--muted);
                font-size: 0.85rem;
                padding: 2rem 0 1rem;
                border-top: 1px solid var(--border);
                margin-top: 3rem;
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
        """.replace("__THEME_VARS__", theme_vars),
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
    """Return dark mode state from query params."""
    theme = st.query_params.get("theme", "light")
    if isinstance(theme, list):
        theme = theme[0] if theme else "light"

    return str(theme).lower() == "dark"


def render_theme_toggle() -> bool:
    """Render theme toggle at top-right and return current dark mode state."""
    if "ui_dark_mode" not in st.session_state:
        st.session_state["ui_dark_mode"] = get_active_theme()

    _, right_col = st.columns([0.82, 0.18])
    with right_col:
        st.markdown("<div class='theme-toggle-wrap'>", unsafe_allow_html=True)
        dark_mode = st.toggle("Dark Mode", key="ui_dark_mode")
        st.markdown("</div>", unsafe_allow_html=True)

    desired_theme = "dark" if dark_mode else "light"
    if st.query_params.get("theme") != desired_theme:
        st.query_params["theme"] = desired_theme

    return bool(dark_mode)


def _build_page_href(page_key: str, dark_mode: bool) -> str:
    theme = "dark" if dark_mode else "light"
    return f"?page={page_key}&theme={theme}"


def render_navbar(active_page: str, dark_mode: bool) -> None:
    """Render the top navigation bar."""
    nav_items = []
    for page_key, label in PAGE_ROUTES.items():
        href = _build_page_href(page_key, dark_mode)
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
    st.sidebar.caption("Designed for fast fake-review screening across multiple sources.")


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
