"""
UI components for displaying metrics, charts, and results.
"""

from typing import Any, Dict, List

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from config import COLORS
from utils import format_confidence, format_metric


def display_metrics_table(
    individual_preds: Dict,
    confidences: Dict,
    metrics: Dict,
    prediction_times: Dict,
    model_names: List[str],
) -> None:
    """
    Display detailed metrics for each model in table format.

    Args:
        individual_preds: Individual model predictions
        confidences: Model confidences
        metrics: Model performance metrics
        prediction_times: Prediction times per model
        model_names: List of model names
    """
    table_data = []

    for model_name in model_names:
        if model_name in individual_preds:
            pred = individual_preds[model_name]
            confidence = confidences.get(model_name, 0.0)
            pred_time = prediction_times.get(model_name, 0.0)

            model_metrics = metrics.get(model_name, {})
            accuracy = model_metrics.get("accuracy", "N/A")
            precision = model_metrics.get("precision", "N/A")
            recall = model_metrics.get("recall", "N/A")
            f1_score = model_metrics.get("f1_score", "N/A")
            sensitivity = model_metrics.get(
                "sensitivity", model_metrics.get("recall", "N/A")
            )

            table_data.append(
                {
                    "Algorithm": model_name,
                    "Prediction": "✅ Genuine" if pred == 1 else "❌ Fake",
                    "Confidence": f"{confidence * 100:.2f}%",
                    "Accuracy": format_metric(accuracy),
                    "Precision": format_metric(precision),
                    "Recall": format_metric(recall),
                    "F1-Score": format_metric(f1_score),
                    "Sensitivity": format_metric(sensitivity),
                    "Time (ms)": f"{pred_time:.2f}",
                }
            )

    if table_data:
        df_metrics = pd.DataFrame(table_data)
        st.dataframe(df_metrics, use_container_width=True, hide_index=True)
    else:
        st.info("No metrics available")


def display_review_metrics_charts(
    individual_preds: Dict,
    confidences: Dict,
    metrics: Dict,
    prediction_times: Dict,
    model_names: List[str],
    key_prefix: str = "",
) -> None:
    """
    Display graphical representations for review metrics.

    Args:
        individual_preds: Individual model predictions
        confidences: Model confidences
        metrics: Model performance metrics
        prediction_times: Prediction times per model
        model_names: List of model names
        key_prefix: Unique key prefix for chart identification
    """
    # Extract confidence and metrics data
    confidence_data = []
    accuracy_data = []
    precision_data = []
    recall_data = []
    f1_data = []

    for model_name in model_names:
        if model_name in confidences:
            confidence_data.append(
                {
                    "model": model_name,
                    "confidence": confidences.get(model_name, 0) * 100,
                }
            )

        model_metrics = metrics.get(model_name, {})
        if any(
            [
                model_metrics.get("accuracy"),
                model_metrics.get("precision"),
                model_metrics.get("recall"),
                model_metrics.get("f1_score"),
            ]
        ):
            accuracy = model_metrics.get("accuracy", 0)
            precision = model_metrics.get("precision", 0)
            recall = model_metrics.get("recall", 0)
            f1_score = model_metrics.get("f1_score", 0)

            accuracy_data.append(accuracy if isinstance(accuracy, float) else 0)
            precision_data.append(precision if isinstance(precision, float) else 0)
            recall_data.append(recall if isinstance(recall, float) else 0)
            f1_data.append(f1_score if isinstance(f1_score, float) else 0)

    col1, col2 = st.columns(2)

    # Chart 1: Model Confidence Levels
    if confidence_data:
        with col1:
            st.markdown("**🎯 Model Confidence Levels**")
            conf_df = pd.DataFrame(confidence_data)
            fig_conf = go.Figure(
                data=[
                    go.Bar(
                        x=conf_df["model"],
                        y=conf_df["confidence"],
                        marker_color=COLORS["confidence"],
                        text=conf_df["confidence"].apply(lambda x: f"{x:.1f}%"),
                        textposition="auto",
                    )
                ]
            )
            fig_conf.update_layout(
                title="",
                xaxis_title="Algorithm",
                yaxis_title="Confidence (%)",
                height=350,
                showlegend=False,
                hovermode="x unified",
            )
            fig_conf.update_yaxes(range=[0, 100])
            st.plotly_chart(
                fig_conf, use_container_width=True, key=f"{key_prefix}_conf"
            )

    # Chart 2: Model Performance Metrics
    if accuracy_data and len(model_names) > 0:
        with col2:
            st.markdown("**📊 Model Performance Metrics**")
            fig_metrics = go.Figure(
                data=[
                    go.Bar(
                        name="Accuracy",
                        x=model_names,
                        y=accuracy_data,
                        marker_color=COLORS["accuracy"],
                    ),
                    go.Bar(
                        name="Precision",
                        x=model_names,
                        y=precision_data,
                        marker_color=COLORS["precision"],
                    ),
                    go.Bar(
                        name="Recall",
                        x=model_names,
                        y=recall_data,
                        marker_color=COLORS["recall"],
                    ),
                    go.Bar(
                        name="F1-Score",
                        x=model_names,
                        y=f1_data,
                        marker_color=COLORS["f1_score"],
                    ),
                ]
            )
            fig_metrics.update_layout(
                title="",
                xaxis_title="Algorithm",
                yaxis_title="Score",
                barmode="group",
                height=350,
                hovermode="x unified",
            )
            fig_metrics.update_yaxes(range=[0, 1])
            st.plotly_chart(
                fig_metrics, use_container_width=True, key=f"{key_prefix}_metrics"
            )

    # Chart 3: Prediction Time Comparison
    if prediction_times:
        st.markdown("**⏱️ Prediction Time Comparison**")
        time_data = []
        for model_name in model_names:
            if model_name in prediction_times:
                time_data.append(
                    {"model": model_name, "time": prediction_times[model_name]}
                )

        if time_data:
            time_df = pd.DataFrame(time_data)
            fig_time = go.Figure(
                data=[
                    go.Bar(
                        x=time_df["model"],
                        y=time_df["time"],
                        marker_color=COLORS["time"],
                        text=time_df["time"].apply(lambda x: f"{x:.2f}ms"),
                        textposition="auto",
                    )
                ]
            )
            fig_time.update_layout(
                title="",
                xaxis_title="Algorithm",
                yaxis_title="Time (ms)",
                height=300,
                showlegend=False,
                hovermode="x unified",
            )
            st.plotly_chart(
                fig_time, use_container_width=True, key=f"{key_prefix}_time"
            )


def display_distribution_chart(genuine_count: int, fake_count: int) -> None:
    """
    Display review distribution pie/bar chart.

    Args:
        genuine_count: Number of genuine reviews
        fake_count: Number of fake reviews
    """
    total = genuine_count + fake_count
    genuine_pct = (genuine_count / total * 100) if total > 0 else 0
    fake_pct = (fake_count / total * 100) if total > 0 else 0

    fig = go.Figure(
        data=[
            go.Bar(
                x=["Genuine", "Fake"],
                y=[genuine_count, fake_count],
                marker_color=[COLORS["genuine"], COLORS["fake"]],
                text=[
                    f"{genuine_count}<br>({genuine_pct:.1f}%)",
                    f"{fake_count}<br>({fake_pct:.1f}%)",
                ],
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title="Review Distribution",
        xaxis_title="Review Type",
        yaxis_title="Count",
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)


def display_summary_metrics(
    total_reviews: int,
    genuine_count: int,
    fake_count: int,
) -> None:
    """
    Display summary metrics in columns.

    Args:
        total_reviews: Total number of reviews
        genuine_count: Number of genuine reviews
        fake_count: Number of fake reviews
    """
    from predictor import get_trust_level

    genuine_pct = (genuine_count / total_reviews * 100) if total_reviews > 0 else 0
    fake_pct = (fake_count / total_reviews * 100) if total_reviews > 0 else 0

    # Pass total_reviews and default confidence for dynamic thresholding
    trust_level = get_trust_level(
        genuine_pct, total_reviews=total_reviews, confidence=0.7
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Reviews", total_reviews)
    with col2:
        st.metric("✅ Genuine", f"{genuine_count} ({genuine_pct:.1f}%)")
    with col3:
        st.metric("❌ Fake", f"{fake_count} ({fake_pct:.1f}%)")
    with col4:
        st.markdown(
            f"<h3 style='text-align: center;'>{trust_level['label']}</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='text-align: center; font-size: 12px; color: #666;'>Authenticity Rating</p>",
            unsafe_allow_html=True,
        )
