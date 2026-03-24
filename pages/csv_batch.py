"""
CSV Batch Analysis page.
"""

from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from config import POSSIBLE_REVIEW_COLUMNS
from predictor import _calculate_confidence, predict_review
from ui.components import (
    display_distribution_chart,
    display_metrics_table,
    display_review_metrics_charts,
    display_summary_metrics,
)
from utils import clean_text, detect_review_column, truncate_text


def show_csv_batch_page(
    models: Dict[str, Any],
    metrics: Dict,
    use_ensemble: bool,
) -> None:
    """
    Display CSV batch analysis interface.

    Args:
        models: Dictionary of loaded models
        metrics: Model metrics dictionary
        use_ensemble: Whether to use ensemble voting
    """
    st.header("📤 CSV Batch Analysis")
    st.markdown("Upload a CSV file containing multiple reviews for batch analysis")

    # Instructions
    with st.expander("📋 CSV Format Instructions"):
        _show_csv_format_instructions()

    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV file containing reviews",
    )

    if uploaded_file is not None:
        try:
            _process_csv_file(uploaded_file, models, metrics, use_ensemble)
        except Exception as e:
            st.error(f"❌ Error processing CSV: {e}")
            st.info("💡 Make sure your CSV has a column with review text.")


def _show_csv_format_instructions() -> None:
    """Display CSV format instructions."""
    st.markdown(
        """
    **Required CSV format:**
    - Must have a column with review text
    - Column name can be: `review_text`, `review`, `text`, `text_`, `Review`, `comment`, etc.
    
    **Example CSV:**
    ```csv
    review_text
    "Great product! Love it."
    "Terrible quality, waste of money!!!"
    "Works as expected, good value."
    ```
    
    **Download Sample CSV:**
    """
    )

    # Create sample CSV
    sample_data = pd.DataFrame(
        {
            "review_text": [
                "I stayed at this hotel last weekend and the staff were very friendly. The room was clean and the breakfast was delicious.",
                "Best product ever!!!! Everyone must buy this now!!! Changed my life instantly!!!!",
                "The phone I bought works perfectly. Battery lasts all day, the screen is bright, and delivery was on time.",
            ]
        }
    )
    sample_csv = sample_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Sample CSV",
        data=sample_csv,
        file_name="sample_reviews.csv",
        mime="text/csv",
    )


def _process_csv_file(
    uploaded_file,
    models: Dict[str, Any],
    metrics: Dict,
    use_ensemble: bool,
) -> None:
    """
    Process uploaded CSV file.

    Args:
        uploaded_file: Uploaded file object
        models: Dictionary of loaded models
        metrics: Model metrics dictionary
        use_ensemble: Whether to use ensemble voting
    """
    # Read CSV
    df_upload = pd.read_csv(uploaded_file)
    st.success(f"✅ File uploaded successfully! Found {len(df_upload)} rows.")

    # Detect review column
    review_column = detect_review_column(df_upload, POSSIBLE_REVIEW_COLUMNS)

    # Let user select if auto-detection fails
    if review_column is None:
        st.warning("⚠️ Could not auto-detect review column. Please select manually:")
        review_column = st.selectbox(
            "Select the column containing reviews:", df_upload.columns
        )
    else:
        st.info(f"📋 Auto-detected review column: **{review_column}**")
        change_col = st.checkbox("Change column selection?")
        if change_col:
            review_column = st.selectbox(
                "Select the column containing reviews:",
                df_upload.columns,
                index=list(df_upload.columns).index(review_column),
            )

    # Show preview
    st.markdown("### 👀 Preview (First 5 rows)")
    st.dataframe(df_upload.head(), use_container_width=True)

    # Analyze button
    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_csv_btn = st.button(
            "🚀 Analyze All Reviews", type="primary", key="analyze_csv"
        )

    if analyze_csv_btn:
        if review_column not in df_upload.columns:
            st.error("❌ Selected column not found in CSV!")
        else:
            batch_results = _analyze_batch_reviews(
                df_upload, review_column, models, use_ensemble
            )

            # Store in session state
            st.session_state["csv_results"] = pd.DataFrame(batch_results)

            # Display results
            _display_batch_results(batch_results, models, metrics, use_ensemble)


def _analyze_batch_reviews(
    df: pd.DataFrame,
    review_column: str,
    models: Dict[str, Any],
    use_ensemble: bool,
) -> List[Dict]:
    """
    Analyze all reviews in batch.

    Args:
        df: DataFrame with reviews
        review_column: Column name containing reviews
        models: Dictionary of loaded models
        use_ensemble: Whether to use ensemble voting

    Returns:
        List of analysis results
    """
    progress_bar = st.progress(0)
    status_text = st.empty()
    batch_results = []

    for row_num, (idx, row) in enumerate(df.iterrows(), start=1):
        review_text = str(row[review_column])

        if review_text and review_text.strip():
            pred, conf, individual_preds, prediction_times, total_time = predict_review(
                review_text, models, ensemble=use_ensemble
            )

            confidences = _get_confidences_for_models(
                models, review_text, individual_preds
            )

            batch_results.append(
                {
                    "Row_Number": row_num,
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
        else:
            batch_results.append(
                {
                    "Row_Number": row_num,
                    "Review": "Empty or invalid",
                    "Prediction": "N/A",
                    "Confidence": "N/A",
                    "Full_Review": "",
                    "Individual_Predictions": {},
                }
            )

        progress_bar.progress(row_num / len(df))
        status_text.text(f"Analyzed {row_num}/{len(df)} reviews...")

    progress_bar.empty()
    status_text.empty()

    return batch_results


def _get_confidences_for_models(
    models: Dict, text: str, individual_preds: Dict
) -> Dict:
    """
    Get confidences for all models.

    Args:
        models: Dictionary of models
        text: Review text
        individual_preds: Individual predictions

    Returns:
        Dictionary of confidences
    """
    confidences = {}
    cleaned = clean_text(text)

    for model_name in individual_preds.keys():
        confidences[model_name] = _calculate_confidence(models[model_name], cleaned)

    return confidences


def _display_batch_results(
    batch_results: List[Dict],
    models: Dict[str, Any],
    metrics: Dict,
    use_ensemble: bool,
) -> None:
    """
    Display batch analysis results.

    Args:
        batch_results: List of analysis results
        models: Dictionary of loaded models
        metrics: Model metrics dictionary
        use_ensemble: Whether ensemble was used
    """
    # Summary
    st.markdown("### 📊 Analysis Summary")

    total_analyzed = len([r for r in batch_results if r["Prediction"] != "N/A"])
    genuine_count = sum(1 for r in batch_results if r["Prediction"] == "Genuine")
    fake_count = sum(1 for r in batch_results if r["Prediction"] == "Fake")

    display_summary_metrics(total_analyzed, genuine_count, fake_count)

    # Visualization
    st.markdown("### 📈 Visualization")
    display_distribution_chart(genuine_count, fake_count)

    # Results table
    st.markdown("### 📋 Detailed Results")

    # Filter
    filter_col1, _ = st.columns(2)
    with filter_col1:
        csv_filter = st.selectbox(
            "Filter by:",
            ["All", "Genuine Only", "Fake Only"],
            key="csv_filter",
        )

    # Apply filter
    df_batch_results = pd.DataFrame(batch_results)
    if csv_filter == "Genuine Only":
        df_csv_display = df_batch_results[
            df_batch_results["Prediction"] == "Genuine"
        ].copy()
    elif csv_filter == "Fake Only":
        df_csv_display = df_batch_results[
            df_batch_results["Prediction"] == "Fake"
        ].copy()
    else:
        df_csv_display = df_batch_results.copy()

    # Display
    st.dataframe(
        df_csv_display[["Row_Number", "Review", "Prediction", "Confidence"]],
        use_container_width=True,
        hide_index=True,
    )

    # Download
    csv_output = df_batch_results.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Analysis Results (CSV)",
        data=csv_output,
        file_name="batch_analysis_results.csv",
        mime="text/csv",
    )

    # Individual reviews
    st.markdown("### 🔎 View Individual Reviews")

    for idx, row in df_csv_display.iterrows():
        if row["Prediction"] != "N/A":
            with st.expander(
                f"Row {row['Row_Number']}: {'✅' if row['Prediction'] == 'Genuine' else '❌'} {row['Prediction']} ({row['Confidence']})"
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

                # Detailed model metrics table
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

                    # Display graphical representations
                    st.markdown("**📈 Visual Analytics:**")
                    display_review_metrics_charts(
                        individual_preds,
                        confidences,
                        metrics,
                        prediction_times,
                        list(individual_preds.keys()),
                        key_prefix=f"csv_review_{idx}",
                    )
                else:
                    st.write("No individual predictions available.")
