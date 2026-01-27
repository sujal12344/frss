
import streamlit as st, pickle, os, re, numpy as np, pandas as pd
from nltk.stem import PorterStemmer

st.set_page_config(page_title="Fake Review Classifier", layout="wide")
st.title("Fake Review Classifier")

MODELS_DIR = "models_pkl"
VISIBLE = ["LogisticRegression","KNeighbors","MultinomialNB"]
ps = PorterStemmer()

def clean_text(s) -> str:
    if s is None: return ""
    s = re.sub(r'http\S+',' ', str(s))
    s = re.sub(r'[^a-zA-Z\s]',' ', s)
    s = re.sub(r'\s+',' ', s).strip().lower()
    toks = [ps.stem(w) for w in s.split()]
    return " ".join(toks)

@st.cache_resource
def list_models() -> list[str]:
    files = [f for f in os.listdir(MODELS_DIR) if f.endswith(".pkl")]
    names = [os.path.splitext(f)[0] for f in files]
    return [n for n in VISIBLE if n in names]

@st.cache_resource
def load_model(name):
    with open(os.path.join(MODELS_DIR, f"{name}.pkl"), "rb") as fh:
        return pickle.load(fh)

@st.cache_resource
def load_metrics():
    with open(os.path.join(MODELS_DIR, "models_summary.pkl"), "rb") as fh:
        return pickle.load(fh)

models = list_models()
if not models:
    st.error("No models found in models_pkl/. Make sure models are present.")
    st.stop()

choice = st.sidebar.selectbox("Select model", models)
show_metrics = st.sidebar.checkbox("Show model metrics", value=True)
show_explain = st.sidebar.checkbox("Show explanation (LogisticRegression only)", value=False)
upload = st.sidebar.file_uploader("Upload CSV for batch prediction", type=["csv"])
ensemble = st.sidebar.checkbox("Use ensemble (majority vote of visible models)", value=False)

col1, col2 = st.columns([2,1])

with col1:
    st.subheader("Classify a single review")
    review = st.text_area("Enter review text:", height=150)
    if st.button("Classify Review"):
        if not review.strip():
            st.warning("Please enter a review.")
        else:
            cleaned = clean_text(review)
            try:
                if ensemble:
                    preds = []
                    probs = []
                    for m in models:
                        model = load_model(m)
                        try:
                            p = model.predict_proba([cleaned])[0]
                            prob = float(max(p))
                        except Exception:
                            try:
                                dfv = model.decision_function([cleaned])
                                prob = float(1/(1+np.exp(-dfv[0])))
                            except Exception:
                                prob = None
                        pr = int(model.predict([cleaned])[0])
                        preds.append(pr); probs.append(prob if prob is not None else 0.0)
                    vote = int(round(sum(preds)/len(preds)))
                    avg_conf = float(sum(probs)/len(probs)) if probs else None
                    if vote == 1:
                        st.success(f"✅ Ensemble: Likely Genuine (vote {sum(preds)}/{len(preds)}). Confidence: {avg_conf:.2f}" if avg_conf else f"✅ Ensemble: Likely Genuine (vote {sum(preds)}/{len(preds)})")
                    else:
                        st.error(f"❌ Ensemble: Likely Fake (vote {sum(preds)}/{len(preds)}). Confidence: {avg_conf:.2f}" if avg_conf else f"❌ Ensemble: Likely Fake (vote {sum(preds)}/{len(preds)})")
                else:
                    model = load_model(choice)
                    try:
                        prob = float(max(model.predict_proba([cleaned])[0]))
                    except Exception:
                        try:
                            dfv = model.decision_function([cleaned])
                            prob = float(1/(1+np.exp(-dfv[0])))
                        except Exception:
                            prob = None
                    pred = int(model.predict([cleaned])[0])
                    if pred == 1:
                        st.success(f"✅ Genuine Review. Confidence: {prob:.2f}" if prob is not None else "✅ Genuine Review.")
                    else:
                        st.error(f"❌ Fake Review. Confidence: {prob:.2f}" if prob is not None else "❌ Fake Review.")

                    if show_explain and choice == "LogisticRegression":
                        try:
                            tfidf = model.named_steps['tfidf']
                            clf = model.named_steps['clf']
                            vec = tfidf.transform([cleaned])
                            feature_names = tfidf.get_feature_names_out()
                            coefs = clf.coef_[0]
                            contrib = (vec.toarray()[0] * coefs)
                            import numpy as np
                            top_idx_pos = np.argsort(contrib)[-10:][::-1]
                            top_idx_neg = np.argsort(contrib)[:10]
                            st.write("Top positive contributing features:")
                            st.write([ (feature_names[i], float(contrib[i])) for i in top_idx_pos if contrib[i]>0 ])
                            st.write("Top negative contributing features:")
                            st.write([ (feature_names[i], float(contrib[i])) for i in top_idx_neg if contrib[i]<0 ])
                        except Exception as e:
                            st.write("Could not compute explanation:", e)

            except Exception as e:
                st.error("Error during prediction: " + str(e))

with col2:
    st.subheader("Model Info")
    st.write("Selected model:", choice)
    if show_metrics:
        try:
            metrics = load_metrics()
            st.json(metrics.get(choice, "No metrics available"))
        except Exception as e:
            st.write("Could not load metrics:", e)

st.markdown("---")
st.subheader("Batch classify from CSV")
if upload is not None:
    try:
        df = pd.read_csv(upload)
        text_cols = [c for c in df.columns if 'review' in c.lower() or 'text' in c.lower() or 'body' in c.lower()]
        if not text_cols:
            st.error("No text column detected in CSV.")
        else:
            text_col = text_cols[0]
            df['cleaned_text'] = df[text_col].astype(str).apply(clean_text)
            if ensemble:
                preds = []
                for m in models:
                    model = load_model(m)
                    try:
                        pr = model.predict(df['cleaned_text'].tolist())
                    except Exception:
                        pr = [0]*len(df)
                    preds.append(pr)
                import numpy as np
                arr = np.array(preds)
                votes = arr.sum(axis=0)
                final = (votes >= (arr.shape[0]/2)).astype(int)
                df['prediction'] = final
            else:
                model = load_model(choice)
                df['prediction'] = model.predict(df['cleaned_text'].tolist())
            df['label_readable'] = df['prediction'].apply(lambda x: "Genuine" if int(x)==1 else "Fake")
            st.write(df.head(20))
            st.download_button("Download predictions", data=df.to_csv(index=False).encode('utf-8'),
                               file_name="predictions.csv", mime="text/csv")
    except Exception as e:
        st.error("Error processing CSV: " + str(e))

st.markdown("### Sample reviews")
st.write("- I stayed at this hotel last weekend and the staff were very friendly. The room was clean and the breakfast was delicious.")
st.write("- Best product ever!!!! Everyone must buy this now!!! Changed my life instantly!!!!")
