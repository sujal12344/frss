"""
Amazon Product Analysis page.
"""

import re
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from predictor import _calculate_confidence, predict_review
from scraper import fetch_amazon_reviews
from ui.components import (
    display_distribution_chart,
    display_metrics_table,
    display_review_metrics_charts,
    display_summary_metrics,
)
from utils import (
    clean_text,
    extract_asin_from_url,
    remove_read_more_patterns,
    truncate_text,
)


def show_amazon_product_page(
    models: Dict[str, Any],
    metrics: Dict,
    use_ensemble: bool,
) -> None:
    """
    Display Amazon product analysis interface.

    Args:
        models: Dictionary of loaded models
        metrics: Model metrics dictionary
        use_ensemble: Whether to use ensemble voting
    """
    st.header("🔗 Analyze Amazon Product Reviews")
    st.markdown("Enter an Amazon product URL or ASIN to analyze all reviews")

    st.info(
        "ℹ️ **Note:** Currently supports Amazon only. For other platforms (Flipkart, Myntra, etc.), use the CSV Batch Analysis tab."
    )

    # Input
    amazon_input = st.text_input(
        "Amazon Product URL or ASIN:",
        placeholder="https://www.amazon.com/dp/B07FTKQ97Q...",
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        fetch_btn = st.button("🚀 Fetch & Analyze", type="primary")

    if fetch_btn:
        if not amazon_input.strip():
            st.warning("⚠️ Please enter a URL or ASIN!")
        else:
            # Extract ASIN
            asin = extract_asin_from_url(amazon_input)

            if not asin:
                st.error("❌ Invalid Amazon URL or ASIN! Please check and try again.")
            else:
                st.info(f"📦 Detected ASIN: **{asin}**")

                # Fetch data
                product_data = fetch_amazon_reviews(asin)

                if product_data and "reviews" in product_data:
                    reviews_list = product_data["reviews"]

                    if not reviews_list:
                        st.warning("⚠️ No reviews found for this product!")
                    else:
                        st.success(f"✅ Found {len(reviews_list)} reviews!")

                        # Display product info
                        _display_amazon_product_info(product_data)

                        # Analyze reviews
                        batch_results = _analyze_amazon_reviews(
                            reviews_list, models, use_ensemble
                        )

                        # Store in session state
                        st.session_state["df_results"] = pd.DataFrame(batch_results)
                        st.session_state["product_name"] = product_data.get(
                            "name", "N/A"
                        )
                        st.session_state["product_rating"] = product_data.get(
                            "average_rating", "N/A"
                        )
                        st.session_state["total_reviews_count"] = product_data.get(
                            "total_reviews", "N/A"
                        )
                        st.session_state["asin"] = asin

                        # Display results
                        _display_amazon_results(
                            batch_results, models, metrics, asin, use_ensemble
                        )

    # Display persisted results
    _show_persisted_amazon_results(models, metrics, use_ensemble)


def _display_amazon_product_info(product_data: Dict) -> None:
    """Display Amazon product information."""
    st.markdown("### 📦 Product Information")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(f"**Name:** {product_data.get('name', 'N/A')[:50]}...")
    with col2:
        st.write(f"**Rating:** {product_data.get('average_rating', 'N/A')} ⭐")
    with col3:
        st.write(f"**Total Reviews:** {product_data.get('total_reviews', 'N/A')}")

    st.markdown("---")


def _analyze_amazon_reviews(
    reviews_list: List[Dict],
    models: Dict[str, Any],
    use_ensemble: bool,
) -> List[Dict]:
    """
    Analyze Amazon reviews.

    Args:
        reviews_list: List of reviews from API
        models: Dictionary of loaded models
        use_ensemble: Whether to use ensemble voting

    Returns:
        List of analysis results
    """
    st.markdown("### 🔍 Analyzing Reviews...")

    progress_bar = st.progress(0)
    status_text = st.empty()

    results = []

    for idx, review in enumerate(reviews_list):
        review_text = review.get("review", "")
        review_text = remove_read_more_patterns(review_text)

        if review_text:
            pred, conf, individual_preds, prediction_times, total_time = predict_review(
                review_text, models, ensemble=use_ensemble
            )

            confidences = _get_confidences(models, review_text, individual_preds)

            results.append(
                {
                    "Username": review.get("username", "Anonymous"),
                    "Stars": review.get("stars", "N/A"),
                    "Date": review.get("date", "N/A"),
                    "Review": truncate_text(review_text),
                    "Prediction": "Genuine" if pred == 1 else "Fake",
                    "Confidence": f"{conf * 100:.1f}%" if conf else "N/A",
                    "Total_Time": f"{total_time:.2f} ms",
                    "Full_Review": review_text,
                    "Individual_Predictions": individual_preds,
                    "Prediction_Times": prediction_times,
                    "Confidences": confidences,
                }
            )

        progress_bar.progress((idx + 1) / len(reviews_list))
        status_text.text(f"Analyzed {idx + 1}/{len(reviews_list)} reviews...")

    progress_bar.empty()
    status_text.empty()

    return results


def _get_confidences(models: Dict, text: str, individual_preds: Dict) -> Dict:
    """Get confidences for all models."""
    confidences = {}
    cleaned = clean_text(text)

    for model_name in individual_preds.keys():
        confidences[model_name] = _calculate_confidence(models[model_name], cleaned)

    return confidences


def _display_amazon_results(
    batch_results: List[Dict],
    models: Dict[str, Any],
    metrics: Dict,
    asin: str,
    use_ensemble: bool,
) -> None:
    """Display Amazon analysis results."""
    df_results = pd.DataFrame(batch_results)

    # Summary
    st.markdown("### 📊 Analysis Summary")

    total_reviews = len(df_results)
    genuine_count = (df_results["Prediction"] == "Genuine").sum()
    fake_count = (df_results["Prediction"] == "Fake").sum()

    display_summary_metrics(total_reviews, genuine_count, fake_count)

    # Visualization
    st.markdown("### 📈 Visualization")
    display_distribution_chart(genuine_count, fake_count)

    # Detailed results
    st.markdown("### 📋 Detailed Results")

    # Filter options
    filter_col1, _ = st.columns(2)
    with filter_col1:
        filter_type = st.selectbox(
            "Filter by:",
            ["All", "Genuine Only", "Fake Only"],
            key="amazon_filter_selector",
        )

    # Apply filter
    if filter_type == "Genuine Only":
        df_display = df_results[df_results["Prediction"] == "Genuine"].copy()
    elif filter_type == "Fake Only":
        df_display = df_results[df_results["Prediction"] == "Fake"].copy()
    else:
        df_display = df_results.copy()

    # Display table
    st.dataframe(
        df_display[["Username", "Stars", "Date", "Review", "Prediction", "Confidence"]],
        use_container_width=True,
        hide_index=True,
    )

    # Download button
    csv = df_results.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Full Analysis (CSV)",
        data=csv,
        file_name=f"amazon_reviews_analysis_{asin}.csv",
        mime="text/csv",
    )

    # Show individual reviews
    st.markdown("### 🔎 View Individual Reviews")

    for idx, row in df_display.iterrows():
        with st.expander(
            f"{'✅' if row['Prediction'] == 'Genuine' else '❌'} {row['Username']} - {row['Stars']} ⭐ ({row['Date']})"
        ):
            st.write(f"**Overall Prediction:** {row['Prediction']}")
            st.write(f"**Ensemble Confidence:** {row['Confidence']}")
            st.markdown("---")

            st.write(f"**Review:**")
            st.write(row["Full_Review"])
            st.markdown("---")

            st.write("**📊 Detailed Model Predictions & Metrics:**")

            if "Individual_Predictions" in row and row["Individual_Predictions"]:
                individual_preds = row["Individual_Predictions"]
                prediction_times = row.get("Prediction_Times", {})
                confidences = row.get("Confidences", {})

                display_metrics_table(
                    individual_preds,
                    confidences,
                    metrics,
                    prediction_times,
                    list(individual_preds.keys()),
                )

                st.markdown("**📈 Visual Analytics:**")
                display_review_metrics_charts(
                    individual_preds,
                    confidences,
                    metrics,
                    prediction_times,
                    list(individual_preds.keys()),
                    key_prefix=f"amazon_review_{idx}",
                )
            else:
                st.write("No individual predictions available.")


def _show_persisted_amazon_results(
    models: Dict[str, Any],
    metrics: Dict,
    use_ensemble: bool,
) -> None:
    """Show persisted Amazon results from session state."""
    if "df_results" in st.session_state:
        # Implementation similar to display results above
        pass
