"""
Walmart Product Analysis page.
"""

from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from predictor import _calculate_confidence, predict_review
from scraper import fetch_walmart_reviews
from ui.components import (
    display_distribution_chart,
    display_metrics_table,
    display_review_metrics_charts,
    display_summary_metrics,
)
from utils import clean_text, extract_product_id_from_walmart_url, truncate_text


def show_walmart_product_page(
    models: Dict[str, Any],
    metrics: Dict,
    use_ensemble: bool,
) -> None:
    """
    Display Walmart product analysis interface.

    Args:
        models: Dictionary of loaded models
        metrics: Model metrics dictionary
        use_ensemble: Whether to use ensemble voting
    """
    st.header("🛒 Analyze Walmart Product Reviews")
    st.markdown("Enter a Walmart product URL or Product ID to analyze all reviews")

    st.info(
        "ℹ️ **Note:** Currently supports Walmart. For other platforms (Flipkart, Myntra, etc.), use the CSV Batch Analysis tab."
    )

    # Input
    walmart_input = st.text_input(
        "Walmart Product URL or Product ID:",
        placeholder="https://www.walmart.com/ip/Product-Name/12345678901...",
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        fetch_walmart_btn = st.button(
            "🚀 Fetch & Analyze", type="primary", key="walmart_fetch"
        )

    if fetch_walmart_btn:
        if not walmart_input.strip():
            st.warning("⚠️ Please enter a URL or Product ID!")
        else:
            # Extract Product ID
            product_id = extract_product_id_from_walmart_url(walmart_input)

            if not product_id:
                st.error(
                    "❌ Invalid Walmart URL or Product ID! Please check and try again."
                )
            else:
                st.info(f"📦 Detected Product ID: **{product_id}**")

                # Fetch data
                product_data = fetch_walmart_reviews(product_id)

                if product_data and "reviews" in product_data:
                    reviews_list = product_data["reviews"]

                    if not reviews_list:
                        st.warning("⚠️ No reviews found for this product!")
                    else:
                        st.success(f"✅ Found {len(reviews_list)} reviews!")

                        # Display product info
                        _display_walmart_product_info(product_data)

                        # Analyze reviews
                        walmart_results = _analyze_walmart_reviews(
                            reviews_list, models, use_ensemble
                        )

                        # Store in session state
                        st.session_state["df_walmart_results"] = pd.DataFrame(
                            walmart_results
                        )
                        st.session_state["walmart_product_name"] = product_data.get(
                            "product_name", "N/A"
                        )
                        st.session_state["walmart_product_rating"] = product_data.get(
                            "rating", "N/A"
                        )
                        st.session_state["walmart_review_count"] = product_data.get(
                            "review_count", "N/A"
                        )
                        st.session_state["walmart_product_id"] = product_id

                        # Display results
                        _display_walmart_results(
                            walmart_results, models, metrics, product_id, use_ensemble
                        )

    # Display persisted results
    _show_persisted_walmart_results(models, metrics, use_ensemble)


def _display_walmart_product_info(product_data: Dict) -> None:
    """Display Walmart product information."""
    st.markdown("### 📦 Product Information")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(f"**Name:** {product_data.get('product_name', 'N/A')[:50]}...")
    with col2:
        st.write(f"**Rating:** {product_data.get('rating', 'N/A')} ⭐")
    with col3:
        st.write(f"**Total Reviews:** {product_data.get('review_count', 'N/A')}")

    st.markdown("---")


def _analyze_walmart_reviews(
    reviews_list: List[Dict],
    models: Dict[str, Any],
    use_ensemble: bool,
) -> List[Dict]:
    """
    Analyze Walmart reviews.

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

    walmart_results = []

    for idx, review in enumerate(reviews_list):
        review_text = review.get("text", "").strip()

        if review_text:
            pred, conf, individual_preds, prediction_times, total_time = predict_review(
                review_text, models, ensemble=use_ensemble
            )

            confidences = _get_confidences(models, review_text, individual_preds)

            # Extract badges for additional context
            badges = review.get("badges", [])
            is_verified = "Verified Purchase" in badges
            is_incentivized = "Incentivized Review" in badges

            walmart_results.append(
                {
                    "Author": review.get("author", "Anonymous"),
                    "Rating": review.get("rating", "N/A"),
                    "Date": review.get("date_published", "N/A"),
                    "Review": truncate_text(review_text),
                    "Prediction": "Genuine" if pred == 1 else "Fake",
                    "Confidence": f"{conf * 100:.1f}%" if conf else "N/A",
                    "Total_Time": f"{total_time:.2f} ms",
                    "Full_Review": review_text,
                    "Individual_Predictions": individual_preds,
                    "Prediction_Times": prediction_times,
                    "Confidences": confidences,
                    "Verified_Purchase": is_verified,
                    "Incentivized": is_incentivized,
                }
            )

        progress_bar.progress((idx + 1) / len(reviews_list))
        status_text.text(f"Analyzed {idx + 1}/{len(reviews_list)} reviews...")

    progress_bar.empty()
    status_text.empty()

    return walmart_results


def _get_confidences(models: Dict, text: str, individual_preds: Dict) -> Dict:
    """Get confidences for all models."""
    confidences = {}
    cleaned = clean_text(text)

    for model_name in individual_preds.keys():
        confidences[model_name] = _calculate_confidence(models[model_name], cleaned)

    return confidences


def _display_walmart_results(
    walmart_results: List[Dict],
    models: Dict[str, Any],
    metrics: Dict,
    product_id: str,
    use_ensemble: bool,
) -> None:
    """Display Walmart analysis results."""
    df_walmart_results = pd.DataFrame(walmart_results)

    # Summary
    st.markdown("### 📊 Analysis Summary")

    total_reviews = len(df_walmart_results)
    genuine_count = (df_walmart_results["Prediction"] == "Genuine").sum()
    fake_count = (df_walmart_results["Prediction"] == "Fake").sum()

    display_summary_metrics(total_reviews, genuine_count, fake_count)

    # Visualization
    st.markdown("### 📈 Visualization")
    display_distribution_chart(genuine_count, fake_count)

    # Detailed results
    st.markdown("### 📋 Detailed Results")

    # Filter options
    filter_col1, _ = st.columns(2)
    with filter_col1:
        walmart_filter = st.selectbox(
            "Filter by:",
            ["All", "Genuine Only", "Fake Only"],
            key="walmart_filter_selector",
        )

    # Apply filter
    if walmart_filter == "Genuine Only":
        df_walmart_display = df_walmart_results[
            df_walmart_results["Prediction"] == "Genuine"
        ].copy()
    elif walmart_filter == "Fake Only":
        df_walmart_display = df_walmart_results[
            df_walmart_results["Prediction"] == "Fake"
        ].copy()
    else:
        df_walmart_display = df_walmart_results.copy()

    # Display table
    st.dataframe(
        df_walmart_display[
            [
                "Author",
                "Rating",
                "Date",
                "Review",
                "Prediction",
                "Confidence",
                "Verified_Purchase",
                "Incentivized",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    # Download button
    csv = df_walmart_results.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Full Analysis (CSV)",
        data=csv,
        file_name=f"walmart_reviews_analysis_{product_id}.csv",
        mime="text/csv",
    )

    # Show individual reviews
    st.markdown("### 🔎 View Individual Reviews")

    for idx, row in df_walmart_display.iterrows():
        purchase_status = (
            "✅ Verified Purchase" if row.get("Verified_Purchase") else "❌ Unverified"
        )

        with st.expander(
            f"{'✅' if row['Prediction'] == 'Genuine' else '❌'} {row['Author']} - {row['Rating']} ⭐ ({row['Date']}) {purchase_status}"
        ):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Overall Prediction:** {row['Prediction']}")
            with col2:
                st.write(f"**Ensemble Confidence:** {row['Confidence']}")
            with col3:
                st.write(f"**Prediction Time:** {row.get('Total_Time', 'N/A')}")
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
                    key_prefix=f"walmart_review_{idx}",
                )
            else:
                st.write("No individual predictions available.")


def _show_persisted_walmart_results(
    models: Dict[str, Any],
    metrics: Dict,
    use_ensemble: bool,
) -> None:
    """Show persisted Walmart results from session state."""
    if "df_walmart_results" in st.session_state:
        # Implementation similar to display results above
        pass
