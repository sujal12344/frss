from predictor import (
    _calculate_confidence,
    _ensemble_prediction,
    get_prediction_label,
    get_trust_level,
    predict_review,
)


class ProbModel:
    def __init__(self, pred=1, prob=0.9):
        self._pred = pred
        self._prob = prob

    def predict(self, values):
        return [self._pred]

    def predict_proba(self, values):
        return [[1 - self._prob, self._prob]]


class DecisionOnlyModel:
    def __init__(self, pred=1, score=1.0):
        self._pred = pred
        self._score = score

    def predict(self, values):
        return [self._pred]

    def decision_function(self, values):
        return [self._score]


class BrokenModel:
    def predict(self, values):
        raise RuntimeError("model failed")


def test_calculate_confidence_from_predict_proba():
    model = ProbModel(pred=1, prob=0.8)
    assert _calculate_confidence(model, "sample") == 0.8


def test_calculate_confidence_from_decision_function_fallback():
    model = DecisionOnlyModel(pred=0, score=0)
    conf = _calculate_confidence(model, "sample")
    assert 0.49 <= conf <= 0.51


def test_calculate_confidence_default_fallback():
    class NoConfidence:
        def predict(self, values):
            return [1]

    assert _calculate_confidence(NoConfidence(), "sample") == 0.5


def test_predict_review_ensemble_majority_vote():
    models = {
        "a": ProbModel(pred=1, prob=0.8),
        "b": ProbModel(pred=1, prob=0.7),
        "c": ProbModel(pred=0, prob=0.6),
    }
    pred, conf, individual, times, total = predict_review("Nice product", models, ensemble=True)
    assert pred == 1
    assert len(individual) == 3
    assert 0.0 <= conf <= 1.0
    assert total >= 0.0
    assert set(times.keys()) == {"a", "b", "c"}


def test_predict_review_single_model_no_ensemble():
    models = {"only": ProbModel(pred=0, prob=0.88)}
    pred, conf, individual, _, _ = predict_review("Bad item", models, ensemble=False)
    assert pred == 0
    assert conf == 0.88
    assert individual == {"only": 0}


def test_predict_review_empty_text_returns_defaults():
    pred, conf, individual, times, total = predict_review("   ", {"m": ProbModel()})
    assert pred == 0
    assert conf == 0.0
    assert individual == {}
    assert times == {}
    assert total == 0.0


def test_predict_review_handles_all_model_failures():
    pred, conf, individual, times, total = predict_review("text", {"bad": BrokenModel()})
    assert pred == 0
    assert conf == 0.0
    assert individual == {}
    assert times == {}
    assert total >= 0.0


def test_ensemble_prediction_helper():
    pred, conf = _ensemble_prediction({"a": 1, "b": 0, "c": 1}, {"a": 0.7, "b": 0.5, "c": 0.9})
    assert pred == 1
    assert abs(conf - 0.7) < 1e-9


def test_prediction_label_and_trust_level():
    assert get_prediction_label(1)["full_label"] == "Genuine"
    assert get_prediction_label(0)["full_label"] == "Fake"
    assert get_trust_level(80)["label"] == "TRUSTWORTHY"
    assert get_trust_level(55)["label"] == "MODERATE"
    assert get_trust_level(20)["label"] == "SUSPICIOUS"
