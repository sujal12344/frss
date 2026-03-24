"""
Model loading and management functionality.
"""

import os
import pickle
from typing import Any, Dict

import streamlit as st

from config import MODELS_DIR


@st.cache_resource
def load_available_models() -> Dict[str, Any]:
    """
    Load all available trained models from the models directory.

    Returns:
        Dictionary of loaded models {model_name: model_object}
    """
    models = {}

    if not os.path.exists(MODELS_DIR):
        st.error(f"❌ Models directory '{MODELS_DIR}' not found!")
        return models

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
def load_model_metrics() -> Dict[str, Dict[str, Any]]:
    """
    Load model performance metrics.

    Returns:
        Dictionary of model metrics
    """
    metrics_path = os.path.join(MODELS_DIR, "models_summary.pkl")

    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            st.warning(f"⚠️ Could not load metrics: {e}")
            return {}

    return {}


def get_model_metric(
    metrics: Dict, model_name: str, metric_key: str, default: Any = "N/A"
) -> Any:
    """
    Safely get a metric value from the metrics dictionary.

    Args:
        metrics: Metrics dictionary
        model_name: Name of the model
        metric_key: Key of the metric
        default: Default value if not found

    Returns:
        Metric value or default
    """
    if model_name not in metrics:
        return default

    model_metrics = metrics[model_name]
    return model_metrics.get(metric_key, default)
    model_metrics = metrics[model_name]
    return model_metrics.get(metric_key, default)
