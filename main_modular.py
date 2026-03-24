"""
Fake Review Detection - Main Application Entry Point
Streamlit app for detecting fake reviews using ensemble ML models.
"""

from typing import Literal

import streamlit as st

from config import MESSAGES, PAGE_CONFIG
from model_handler import load_available_models, load_model_metrics
from pages.amazon_product import show_amazon_product_page
from pages.csv_batch import show_csv_batch_page
from pages.single_review import show_single_review_page
from pages.walmart_product import show_walmart_product_page


def initialize_app() -> None:
    """Initialize Streamlit page configuration."""
    st.set_page_config(
        page_title=PAGE_CONFIG["page_title"],
        layout=PAGE_CONFIG["layout"] or "wide",  # type: ignore
        initial_sidebar_state=PAGE_CONFIG["initial_sidebar_state"] or "expanded",  # type: ignore
    )
    st.title("Fake Review Detector")
    st.markdown("**Detect fake reviews using ML models trained on 1M+ reviews**")
    st.markdown("---")


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

    st.success(f"✅ Loaded {len(models)} models: {', '.join(models.keys())}")
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
    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: gray;'>
        <p>🎓 Powered by Machine Learning | Trained on 1M+ Reviews</p>
        <p>Supports: Amazon, Walmart, CSV Batch Analysis & Single Review Detection</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def main() -> None:
    """Main application entry point."""
    # Initialize app
    initialize_app()

    # Load resources
    models, metrics = load_resources()

    # Setup sidebar
    use_ensemble, selected_model, show_model_details = setup_sidebar(models)
    display_model_metrics_sidebar(models, metrics, show_model_details)

    # Show tabs
    show_tabs(models, metrics, use_ensemble, selected_model)

    # Show footer
    show_footer()


if __name__ == "__main__":
    main()
    main()
