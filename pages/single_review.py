"""
Single Review Analysis page.
"""

from typing import Any, Dict

import streamlit as st

from predictor import _calculate_confidence, predict_review
from ui.components import (
    display_distribution_chart,
    display_metrics_table,
    display_review_metrics_charts,
)
from utils import clean_text


def show_single_review_page(
    models: Dict[str, Any],
    metrics: Dict,
    use_ensemble: bool,
    selected_model: str,
) -> None:
    """
    Display single review analysis interface.

    Args:
        models: Dictionary of loaded models
        metrics: Model metrics dictionary
        use_ensemble: Whether to use ensemble voting
        selected_model: Selected single model name
    """
    st.header("✍️ Analyze a Single Review")

    review_text = st.text_area(
        "Enter review text:",
        height=150,
        placeholder="Type or paste a review here...",
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_btn = st.button("🔍 Analyze Review", type="primary")

    if analyze_btn:
        if not review_text.strip():
            st.warning("⚠️ Please enter a review text!")
        else:
            with st.spinner("🔄 Analyzing review..."):
                if use_ensemble:
                    pred, conf, individual_preds, prediction_times, total_time = (
                        predict_review(review_text, models, ensemble=True)
                    )
                    confidences = _get_model_confidences(
                        models, review_text, individual_preds
                    )
                else:
                    pred, conf, individual_preds, prediction_times, total_time = (
                        predict_review(
                            review_text,
                            {selected_model: models[selected_model]},
                            ensemble=False,
                        )
                    )
                    confidences = {selected_model: conf}

            if pred is not None:
                _display_single_review_result(
                    pred,
                    conf,
                    total_time,
                    use_ensemble,
                    individual_preds,
                    confidences,
                    prediction_times,
                    metrics,
                )
            else:
                st.error("❌ Could not analyze the review!")


def _get_model_confidences(models: Dict, text: str, individual_preds: Dict) -> Dict:
    """
    Calculate confidences for all models.

    Args:
        models: Dictionary of models
        text: Cleaned text
        individual_preds: Individual predictions

    Returns:
        Dictionary of confidences
    """
    confidences = {}
    cleaned = clean_text(text)

    for model_name in individual_preds.keys():
        confidences[model_name] = _calculate_confidence(models[model_name], cleaned)

    return confidences


def _display_single_review_result(
    pred: int,
    conf: float,
    total_time: float,
    use_ensemble: bool,
    individual_preds: Dict,
    confidences: Dict,
    prediction_times: Dict,
    metrics: Dict,
) -> None:
    """
    Display single review analysis result.

    Args:
        pred: Prediction (0=Fake, 1=Genuine)
        conf: Confidence score
        total_time: Total prediction time
        use_ensemble: Whether ensemble was used
        individual_preds: Individual model predictions
        confidences: Model confidences
        prediction_times: Prediction times
        metrics: Model metrics
    """
    st.markdown("### 📊 Analysis Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        if pred == 1:
            st.success("### ✅ GENUINE")
        else:
            st.error("### ❌ FAKE")

    with col2:
        confidence_display = f"{conf * 100:.1f}%" if conf is not None else "N/A"
        st.metric("Confidence", confidence_display)

    with col3:
        st.metric("Total Prediction Time", f"{total_time:.2f} ms")

    # Individual model predictions metrics table
    if use_ensemble and len(individual_preds) > 1:
        st.markdown("### 🤖 Detailed Model Predictions")
        display_metrics_table(
            individual_preds,
            confidences,
            metrics,
            prediction_times,
            list(individual_preds.keys()),
        )

        # Display graphical representations
        st.markdown("### 📈 Visual Analytics")
        display_review_metrics_charts(
            individual_preds,
            confidences,
            metrics,
            prediction_times,
            list(individual_preds.keys()),
            key_prefix="single_review",
        )
