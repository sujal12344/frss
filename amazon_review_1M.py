"""
🎯 Fake Review Detector
- Single review detection
- Batch analysis from Amazon product URL
- Uses trained models from models_1M_pkl/
"""

import os
import pickle
import re

import numpy as np
import pandas as pd
import requests
import streamlit as st
from nltk.stem import PorterStemmer

# Page config
st.set_page_config(page_title="Amazon Review Analyzer", page_icon="🔍", layout="wide")

# Constants
MODELS_DIR = "models_1Ms_pkl"
SCRAPER_API_KEY = "2e3a0b27898501a44e5f18eff3e1775d"
ps = PorterStemmer()

# ==================== HELPER FUNCTIONS ====================


def clean_text(text) -> str:
    """Clean and preprocess text for model prediction"""
    if text is None or pd.isna(text):
        return ""

    text = str(text)

    # Remove "Read more" and similar patterns from scraped reviews
    text = re.sub(r"\s*read\s+more\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*\.\.\.\s*read\s+more\s*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*see\s+more\s*$", "", text, flags=re.IGNORECASE)

    # Remove URLs
    text = re.sub(r"http\S+", " ", text)
    # Remove special characters
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    # Lowercase
    text = text.lower()
    # Stemming
    words = [ps.stem(word) for word in text.split()]

    return " ".join(words)


@st.cache_resource
def load_available_models():
    """Load all available trained models from the models directory"""
    models = {}
    if not os.path.exists(MODELS_DIR):
        st.error(f"❌ Models directory '{MODELS_DIR}' not found!")
        return models

    # Dynamically discover all .pkl files in the directory
    try:
        for filename in os.listdir(MODELS_DIR):
            if filename.endswith(".pkl") and filename != "models_summary.pkl":
                model_name = filename[:-4]  # Remove .pkl extension
                model_path = os.path.join(MODELS_DIR, filename)
                try:
                    with open(model_path, "rb") as f:
                        models[model_name] = pickle.load(f)
                except Exception as e:
                    st.warning(f"⚠️ Could not load {model_name}: {e}")
    except Exception as e:
        st.error(f"❌ Error scanning models directory: {e}")

    return models


@st.cache_resource
def load_model_metrics():
    """Load model performance metrics"""
    metrics_path = os.path.join(MODELS_DIR, "models_summary.pkl")
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, "rb") as f:
                return pickle.load(f)
        except:
            return {}
    return {}


def predict_review(text, models, ensemble=True):
    """
    Predict if a review is Fake or Genuine
    Returns: prediction (0=Fake, 1=Genuine), confidence, individual predictions
    """
    cleaned = clean_text(text)

    if not cleaned:
        return None, None, {}

    predictions = {}
    confidences = {}

    for model_name, model in models.items():
        try:
            # Get prediction
            pred = int(model.predict([cleaned])[0])
            predictions[model_name] = pred

            # Get confidence
            try:
                prob = model.predict_proba([cleaned])[0]
                conf = float(max(prob))
            except:
                try:
                    dfv = model.decision_function([cleaned])
                    conf = float(1 / (1 + np.exp(-dfv[0])))
                except:
                    conf = 0.5

            confidences[model_name] = conf
        except Exception as e:
            st.warning(f"Error with {model_name}: {e}")

    if ensemble and len(predictions) > 0:
        # Majority voting
        vote_count = sum(predictions.values())
        final_pred = 1 if vote_count >= len(predictions) / 2 else 0
        avg_conf = sum(confidences.values()) / len(confidences)
        return final_pred, avg_conf, predictions
    elif len(predictions) > 0:
        # Use first model
        first_model = list(predictions.keys())[0]
        return predictions[first_model], confidences[first_model], predictions
    else:
        return None, None, {}


def extract_asin_from_url(url):
    """Extract ASIN from Amazon URL"""
    # Pattern: /dp/ASIN or /product/ASIN or ?asin=ASIN
    patterns = [
        r"/dp/([A-Z0-9]{10})",
        r"/product/([A-Z0-9]{10})",
        r"[?&]asin=([A-Z0-9]{10})",
        r"/gp/product/([A-Z0-9]{10})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # Check if URL is already an ASIN
    if re.match(r"^[A-Z0-9]{10}$", url.strip()):
        return url.strip()

    return None


def fetch_amazon_reviews(asin):
    """Fetch product reviews from Amazon using ScraperAPI"""
    try:
        payload = {"api_key": SCRAPER_API_KEY, "asin": asin}

        with st.spinner(f"🔄 Fetching reviews for ASIN: {asin}..."):
            response = requests.get(
                "https://api.scraperapi.com/structured/amazon/product/v1",
                params=payload,
                timeout=60,
            )

        if response.status_code == 200:
            data = response.json()
            return data
        if response.status_code == 404:
            st.error("❌ Product not found on Amazon!")
            return None
        else:
            st.error(f"❌ API Error: Status Code {response.status_code}")
            print(f"API Error: {response.text}")
            return None

    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
        print(f"Exception: {str(e)}")
        return None


# ==================== STREAMLIT UI ====================

st.title("Fake Review Detector")
st.markdown("**Detect fake reviews using ML models trained on 1M+ reviews**")
st.markdown("---")

# Load models
models = load_available_models()
metrics = load_model_metrics()

if not models:
    st.error(
        "❌ No models found! Please train models first using `train_model_1M.ipynb`"
    )
    st.stop()

st.success(f"✅ Loaded {len(models)} models: {', '.join(models.keys())}")

# Sidebar
st.sidebar.header("⚙️ Settings")
use_ensemble = st.sidebar.checkbox("🤖 Use Ensemble (Majority Vote)", value=True)
selected_model = st.sidebar.selectbox(
    "📊 Single Model (if not ensemble)", list(models.keys())
)
show_model_details = st.sidebar.checkbox("📈 Show Model Performance", value=False)

if show_model_details and metrics:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Model Metrics")
    for model_name in models.keys():
        if model_name in metrics:
            m = metrics[model_name]
            st.sidebar.write(f"**{model_name}**")
            st.sidebar.write(f"- Accuracy: {m.get('accuracy', 'N/A')}")
            st.sidebar.write(f"- F1-Score: {m.get('f1_score', 'N/A')}")

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Tip:** Ensemble mode combines multiple models for better accuracy!"
)

# Main tabs
tab1, tab2, tab3 = st.tabs(
    ["✍️ Single Review Analysis", "📤 CSV Batch Analysis", "🔗 Amazon Product Analysis"]
)

# ==================== TAB 1: SINGLE REVIEW ====================
with tab1:
    st.header("✍️ Analyze a Single Review")

    review_text = st.text_area(
        "Enter review text:", height=150, placeholder="Type or paste a review here..."
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
                    pred, conf, individual_preds = predict_review(
                        review_text, models, ensemble=True
                    )
                else:
                    pred, conf, individual_preds = predict_review(
                        review_text,
                        {selected_model: models[selected_model]},
                        ensemble=False,
                    )

            if pred is not None:
                # Display result
                st.markdown("### 📊 Analysis Result")

                col1, col2, col3 = st.columns(3)

                with col1:
                    if pred == 1:
                        st.success("### ✅ GENUINE")
                    else:
                        st.error("### ❌ FAKE")

                with col2:
                    confidence_display = (
                        f"{conf*100:.1f}%" if conf is not None else "N/A"
                    )
                    st.metric("Confidence", confidence_display)

                with col3:
                    genuine_votes = sum(1 for p in individual_preds.values() if p == 1)
                    total_votes = len(individual_preds)
                    st.metric(
                        "Model Agreement", f"{genuine_votes}/{total_votes} Genuine"
                    )

                # Individual model predictions
                if use_ensemble and len(individual_preds) > 1:
                    st.markdown("### 🤖 Individual Model Predictions")

                    pred_df = pd.DataFrame(
                        [
                            {
                                "Model": name,
                                "Prediction": "✅ Genuine" if p == 1 else "❌ Fake",
                            }
                            for name, p in individual_preds.items()
                        ]
                    )

                    st.dataframe(pred_df, use_container_width=True, hide_index=True)
            else:
                st.error("❌ Could not analyze the review!")

# ==================== TAB 2: CSV BATCH ANALYSIS ====================
with tab2:
    st.header("📤 CSV Batch Analysis")
    st.markdown("Upload a CSV file containing multiple reviews for batch analysis")

    # Instructions
    with st.expander("📋 CSV Format Instructions"):
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

    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CSV file", type=["csv"], help="Upload a CSV file containing reviews"
    )

    if uploaded_file is not None:
        try:
            # Read CSV
            df_upload = pd.read_csv(uploaded_file)

            st.success(f"✅ File uploaded successfully! Found {len(df_upload)} rows.")

            # Detect review column
            possible_columns = [
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
            review_column = None

            for col in possible_columns:
                if col in df_upload.columns:
                    review_column = col
                    break

            # Let user select if auto-detection fails
            if review_column is None:
                st.warning(
                    "⚠️ Could not auto-detect review column. Please select manually:"
                )
                review_column = st.selectbox(
                    "Select the column containing reviews:", df_upload.columns
                )
            else:
                st.info(f"📋 Auto-detected review column: **{review_column}**")
                # Option to change
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
                    st.markdown("### 🔍 Analyzing Reviews...")

                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    batch_results = []

                    for row_num, (idx, row) in enumerate(df_upload.iterrows(), start=1):
                        review_text = str(row[review_column])

                        if (
                            review_text
                            and not pd.isna(review_text)
                            and review_text.strip()
                        ):
                            pred, conf, individual_preds = predict_review(
                                review_text, models, ensemble=use_ensemble
                            )

                            batch_results.append(
                                {
                                    "Row_Number": row_num,
                                    "Review": (
                                        review_text[:100] + "..."
                                        if len(review_text) > 100
                                        else review_text
                                    ),
                                    "Prediction": "Genuine" if pred == 1 else "Fake",
                                    "Confidence": f"{conf*100:.1f}%" if conf else "N/A",
                                    "Full_Review": review_text,
                                    "Individual_Predictions": individual_preds,
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

                        progress_bar.progress(row_num / len(df_upload))
                        status_text.text(
                            f"Analyzed {row_num}/{len(df_upload)} reviews..."
                        )

                    progress_bar.empty()
                    status_text.empty()

                    # Create results DataFrame
                    df_batch_results = pd.DataFrame(batch_results)

                    # Store in session state
                    st.session_state["csv_results"] = df_batch_results

                    # Summary
                    st.markdown("### 📊 Analysis Summary")

                    col1, col2, col3, col4 = st.columns(4)

                    total_analyzed = len(
                        [r for r in batch_results if r["Prediction"] != "N/A"]
                    )
                    genuine_count = sum(
                        1 for r in batch_results if r["Prediction"] == "Genuine"
                    )
                    fake_count = sum(
                        1 for r in batch_results if r["Prediction"] == "Fake"
                    )
                    genuine_pct = (
                        (genuine_count / total_analyzed * 100)
                        if total_analyzed > 0
                        else 0
                    )
                    fake_pct = (
                        (fake_count / total_analyzed * 100) if total_analyzed > 0 else 0
                    )

                    with col1:
                        st.metric("Total Analyzed", total_analyzed)
                    with col2:
                        st.metric("✅ Genuine", f"{genuine_count} ({genuine_pct:.1f}%)")
                    with col3:
                        st.metric("❌ Fake", f"{fake_count} ({fake_pct:.1f}%)")
                    with col4:
                        if genuine_pct >= 70:
                            st.success("🟢 TRUSTWORTHY")
                        elif genuine_pct >= 50:
                            st.warning("🟡 MODERATE")
                        else:
                            st.error("🔴 SUSPICIOUS")

                    # Visualization
                    st.markdown("### 📈 Visualization")

                    import plotly.graph_objects as go

                    fig = go.Figure(
                        data=[
                            go.Bar(
                                x=["Genuine", "Fake"],
                                y=[genuine_count, fake_count],
                                marker_color=["#2ecc71", "#e74c3c"],
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

                    # Results table
                    st.markdown("### 📋 Detailed Results")

                    # Filter
                    filter_col1, filter_col2 = st.columns(2)
                    with filter_col1:
                        csv_filter = st.selectbox(
                            "Filter by:",
                            ["All", "Genuine Only", "Fake Only"],
                            key="csv_filter",
                        )

                    # Apply filter
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
                        df_csv_display[
                            ["Row_Number", "Review", "Prediction", "Confidence"]
                        ],
                        use_container_width=True,
                        hide_index=True,
                    )

                    # Download
                    csv_output = df_batch_results.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="📥 Download Analysis Results (CSV)",
                        data=csv_output,
                        file_name=f"batch_analysis_results.csv",
                        mime="text/csv",
                    )

                    # Individual reviews
                    st.markdown("### 🔎 View Individual Reviews")

                    for idx, row in df_csv_display.iterrows():
                        if row["Prediction"] != "N/A":
                            with st.expander(
                                f"Row {row['Row_Number']}: {'✅' if row['Prediction'] == 'Genuine' else '❌'} {row['Prediction']} ({row['Confidence']})"
                            ):
                                st.write(f"**Overall Prediction:** {row['Prediction']}")
                                st.write(
                                    f"**Ensemble Confidence:** {row['Confidence']}"
                                )
                                st.markdown("---")

                                st.write(f"**Review:**")
                                st.write(row["Full_Review"])
                                st.markdown("---")

                                # Individual model predictions
                                st.write("**🤖 Individual Model Predictions:**")

                                if (
                                    "Individual_Predictions" in row
                                    and row["Individual_Predictions"]
                                ):
                                    individual_preds = row["Individual_Predictions"]

                                    num_models = len(individual_preds)
                                    cols = st.columns(min(num_models, 3))

                                    for i, (model_name, pred) in enumerate(
                                        individual_preds.items()
                                    ):
                                        col_idx = i % 3
                                        with cols[col_idx]:
                                            if pred == 1:
                                                st.success(
                                                    f"**{model_name}**\n✅ Genuine"
                                                )
                                            else:
                                                st.error(f"**{model_name}**\n❌ Fake")
                                else:
                                    st.write("No individual predictions available.")

        except Exception as e:
            st.error(f"❌ Error processing CSV: {e}")
            st.info("💡 Make sure your CSV has a column with review text.")

# ==================== TAB 3: AMAZON PRODUCT ====================
with tab3:
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

                        # Product info
                        st.markdown("### 📦 Product Information")
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.write(
                                f"**Name:** {product_data.get('name', 'N/A')[:50]}..."
                            )
                        with col2:
                            st.write(
                                f"**Rating:** {product_data.get('average_rating', 'N/A')} ⭐"
                            )
                        with col3:
                            st.write(
                                f"**Total Reviews:** {product_data.get('total_reviews', 'N/A')}"
                            )

                        st.markdown("---")

                        # Analyze reviews
                        st.markdown("### 🔍 Analyzing Reviews...")

                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        results = []

                        for idx, review in enumerate(reviews_list):
                            review_text = review.get("review", "")

                            # Remove "Read more" from scraped review text
                            review_text = re.sub(
                                r"\s*read\s+more\s*$",
                                "",
                                review_text,
                                flags=re.IGNORECASE,
                            )
                            review_text = re.sub(
                                r"\s*\.\.\.\s*read\s+more\s*$",
                                "",
                                review_text,
                                flags=re.IGNORECASE,
                            )
                            review_text = re.sub(
                                r"\s*see\s+more\s*$",
                                "",
                                review_text,
                                flags=re.IGNORECASE,
                            )
                            review_text = review_text.strip()

                            if review_text:
                                pred, conf, individual_preds = predict_review(
                                    review_text, models, ensemble=use_ensemble
                                )

                                results.append(
                                    {
                                        "Username": review.get("username", "Anonymous"),
                                        "Stars": review.get("stars", "N/A"),
                                        "Date": review.get("date", "N/A"),
                                        "Review": (
                                            review_text[:100] + "..."
                                            if len(review_text) > 100
                                            else review_text
                                        ),
                                        "Prediction": (
                                            "Genuine" if pred == 1 else "Fake"
                                        ),
                                        "Confidence": (
                                            f"{conf*100:.1f}%" if conf else "N/A"
                                        ),
                                        "Full_Review": review_text,
                                        "Individual_Predictions": individual_preds,
                                    }
                                )

                            progress_bar.progress((idx + 1) / len(reviews_list))
                            status_text.text(
                                f"Analyzed {idx + 1}/{len(reviews_list)} reviews..."
                            )

                        progress_bar.empty()
                        status_text.empty()

                        # Create DataFrame
                        df_results = pd.DataFrame(results)

                        # Store in session state to prevent reset on filter change
                        st.session_state["df_results"] = df_results
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

                        # Summary
                        st.markdown("### 📊 Analysis Summary")

                        col1, col2, col3, col4 = st.columns(4)

                        total_reviews = len(df_results)
                        genuine_count = (df_results["Prediction"] == "Genuine").sum()
                        fake_count = (df_results["Prediction"] == "Fake").sum()
                        genuine_pct = (
                            (genuine_count / total_reviews * 100)
                            if total_reviews > 0
                            else 0
                        )
                        fake_pct = (
                            (fake_count / total_reviews * 100)
                            if total_reviews > 0
                            else 0
                        )

                        with col1:
                            st.metric("Total Reviews", total_reviews)
                        with col2:
                            st.metric(
                                "✅ Genuine", f"{genuine_count} ({genuine_pct:.1f}%)"
                            )
                        with col3:
                            st.metric("❌ Fake", f"{fake_count} ({fake_pct:.1f}%)")
                        with col4:
                            if genuine_pct >= 70:
                                st.success("🟢 TRUSTWORTHY")
                            elif genuine_pct >= 50:
                                st.warning("🟡 MODERATE")
                            else:
                                st.error("🔴 SUSPICIOUS")

                        # Visualization
                        st.markdown("### 📈 Visualization")

                        import plotly.graph_objects as go

                        fig = go.Figure(
                            data=[
                                go.Bar(
                                    x=["Genuine", "Fake"],
                                    y=[genuine_count, fake_count],
                                    marker_color=["#2ecc71", "#e74c3c"],
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

                        # Detailed results
                        st.markdown("### 📋 Detailed Results")

# Check if we have results in session state (for filter persistence)
if "df_results" in st.session_state and not fetch_btn:
    df_results = st.session_state["df_results"]
    asin = st.session_state.get("asin", "unknown")

    # Show product info from session
    st.markdown("### 📦 Product Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Name:** {st.session_state.get('product_name', 'N/A')[:50]}...")
    with col2:
        st.write(f"**Rating:** {st.session_state.get('product_rating', 'N/A')} ⭐")
    with col3:
        st.write(
            f"**Total Reviews:** {st.session_state.get('total_reviews_count', 'N/A')}"
        )

    st.markdown("---")

    # Summary
    st.markdown("### 📊 Analysis Summary")
    col1, col2, col3, col4 = st.columns(4)

    total_reviews = len(df_results)
    genuine_count = (df_results["Prediction"] == "Genuine").sum()
    fake_count = (df_results["Prediction"] == "Fake").sum()
    genuine_pct = (genuine_count / total_reviews * 100) if total_reviews > 0 else 0
    fake_pct = (fake_count / total_reviews * 100) if total_reviews > 0 else 0

    with col1:
        st.metric("Total Reviews", total_reviews)
    with col2:
        st.metric("✅ Genuine", f"{genuine_count} ({genuine_pct:.1f}%)")
    with col3:
        st.metric("❌ Fake", f"{fake_count} ({fake_pct:.1f}%)")
    with col4:
        if genuine_pct >= 70:
            st.success("🟢 TRUSTWORTHY")
        elif genuine_pct >= 50:
            st.warning("🟡 MODERATE")
        else:
            st.error("🔴 SUSPICIOUS")

    # Visualization
    st.markdown("### 📈 Visualization")
    import plotly.graph_objects as go

    fig = go.Figure(
        data=[
            go.Bar(
                x=["Genuine", "Fake"],
                y=[genuine_count, fake_count],
                marker_color=["#2ecc71", "#e74c3c"],
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

    # Detailed results
    st.markdown("### 📋 Detailed Results")

    # Filter options
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        filter_type = st.selectbox(
            "Filter by:", ["All", "Genuine Only", "Fake Only"], key="filter_selector"
        )

    # Apply filter
    if filter_type == "Genuine Only":
        df_display = df_results[df_results["Prediction"] == "Genuine"].copy()
    elif filter_type == "Fake Only":
        df_display = df_results[df_results["Prediction"] == "Fake"].copy()
    else:
        df_display = df_results.copy()

    # Display table (without Full_Review and Individual_Predictions)
    st.dataframe(
        df_display[
            [
                "Username",
                "Stars",
                "Date",
                "Review",
                "Prediction",
                "Confidence",
            ]
        ],
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

    # Show individual reviews with model predictions
    st.markdown("### 🔎 View Individual Reviews")

    for idx, row in df_display.iterrows():
        with st.expander(
            f"{'✅' if row['Prediction'] == 'Genuine' else '❌'} {row['Username']} - {row['Stars']} ⭐ ({row['Date']})"
        ):
            # Overall prediction
            st.write(f"**Overall Prediction:** {row['Prediction']}")
            st.write(f"**Ensemble Confidence:** {row['Confidence']}")
            st.markdown("---")

            # Full review
            st.write(f"**Review:**")
            st.write(row["Full_Review"])
            st.markdown("---")

            # Individual model predictions
            st.write("**🤖 Individual Model Predictions:**")

            if "Individual_Predictions" in row and row["Individual_Predictions"]:
                individual_preds = row["Individual_Predictions"]

                # Create columns for models
                num_models = len(individual_preds)
                cols = st.columns(min(num_models, 3))

                for i, (model_name, pred) in enumerate(individual_preds.items()):
                    col_idx = i % 3
                    with cols[col_idx]:
                        if pred == 1:
                            st.success(f"**{model_name}**\n✅ Genuine")
                        else:
                            st.error(f"**{model_name}**\n❌ Fake")
            else:
                st.write("No individual predictions available.")

# Footer
st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: gray;'>
    <p>🎓 Powered by Machine Learning | Trained on 1M+ Reviews</p>
    <p>Models: LogisticRegression, MultinomialNB, KNeighbors, LinearSVC, RandomForest</p>
</div>
""",
    unsafe_allow_html=True,
)
