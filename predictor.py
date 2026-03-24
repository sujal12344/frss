"""
Prediction logic and confidence calculation.
"""

import time
from typing import Any, Dict, Tuple

import numpy as np

from utils import clean_text


def predict_review(
    text: str, models: Dict[str, Any], ensemble: bool = True
) -> Tuple[int, float, Dict, Dict, float]:
    """
    Predict if a review is Fake (0) or Genuine (1).

    Args:
        text: Review text to predict
        models: Dictionary of loaded models
        ensemble: Whether to use ensemble voting (default: True)

    Returns:
        Tuple of (prediction, confidence, individual_preds, prediction_times, total_time)
    """
    start_time = time.time()
    cleaned = clean_text(text)

    if not cleaned:
        return 0, 0.0, {}, {}, 0.0

    predictions = {}
    confidences = {}
    prediction_times = {}

    for model_name, model in models.items():
        try:
            model_start = time.time()

            # Get prediction
            pred = int(model.predict([cleaned])[0])
            predictions[model_name] = pred

            # Get confidence
            conf = _calculate_confidence(model, cleaned)
            confidences[model_name] = conf

            prediction_times[model_name] = round(
                (time.time() - model_start) * 1000, 2
            )  # ms
        except Exception as e:
            print(f"Error with {model_name}: {e}")

    total_time = round((time.time() - start_time) * 1000, 2)  # ms

    if ensemble and len(predictions) > 0:
        # Majority voting
        final_pred, avg_conf = _ensemble_prediction(predictions, confidences)
        return final_pred, avg_conf, predictions, prediction_times, total_time
    elif len(predictions) > 0:
        # Use first model
        first_model = list(predictions.keys())[0]
        return (
            predictions[first_model],
            confidences[first_model],
            predictions,
            prediction_times,
            total_time,
        )
    else:
        return 0, 0.0, {}, {}, 0.0


def _calculate_confidence(model: Any, text: str) -> float:
    """
    Calculate confidence score from model.

    Args:
        model: Trained model object
        text: Cleaned text input

    Returns:
        Confidence value between 0 and 1
    """
    try:
        prob = model.predict_proba([text])[0]
        return float(max(prob))
    except:
        try:
            dfv = model.decision_function([text])
            return float(1 / (1 + np.exp(-dfv[0])))
        except:
            return 0.5


def _ensemble_prediction(predictions: Dict, confidences: Dict) -> Tuple[int, float]:
    """
    Combine predictions using majority voting.

    Args:
        predictions: Individual model predictions
        confidences: Individual model confidences

    Returns:
        Tuple of (final_prediction, average_confidence)
    """
    vote_count = sum(predictions.values())
    final_pred = 1 if vote_count >= len(predictions) / 2 else 0
    avg_conf = sum(confidences.values()) / len(confidences)
    return final_pred, avg_conf


def get_prediction_label(prediction: int) -> Dict[str, str]:
    """
    Get label and color for a prediction.

    Args:
        prediction: Prediction value (0=Fake, 1=Genuine)

    Returns:
        Dictionary with label and color
    """
    from config import PREDICTIONS

    return PREDICTIONS.get(prediction, {"label": "Unknown", "color": "gray"})


def get_trust_level(genuine_percentage: float) -> Dict[str, Any]:
    """
    Determine trust level based on genuine percentage.

    Args:
        genuine_percentage: Percentage of genuine reviews

    Returns:
        Dictionary with trust level info
    """
    from config import TRUST_LEVELS

    if genuine_percentage >= TRUST_LEVELS["trustworthy"]["threshold"]:
        return TRUST_LEVELS["trustworthy"]
    elif genuine_percentage >= TRUST_LEVELS["moderate"]["threshold"]:
        return TRUST_LEVELS["moderate"]
    else:
        return TRUST_LEVELS["suspicious"]
