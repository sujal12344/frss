import pandas as pd

import pages.amazon_product as amazon_page
import pages.csv_batch as csv_page
import pages.walmart_product as walmart_page


class DummyProgress:
    def progress(self, _value):
        return None

    def empty(self):
        return None


class DummyStatus:
    def text(self, _value):
        return None

    def empty(self):
        return None


def _patch_streamlit_progress(monkeypatch, module):
    monkeypatch.setattr(module.st, "progress", lambda _initial=0: DummyProgress())
    monkeypatch.setattr(module.st, "empty", lambda: DummyStatus())
    monkeypatch.setattr(module.st, "markdown", lambda _x: None)


def test_analyze_batch_reviews_csv_feature(monkeypatch):
    _patch_streamlit_progress(monkeypatch, csv_page)
    monkeypatch.setattr(
        csv_page,
        "predict_review",
        lambda text, models, ensemble=True: (1, 0.81, {"m1": 1}, {"m1": 1.2}, 3.4),
    )
    monkeypatch.setattr(csv_page, "_get_confidences_for_models", lambda *args, **kwargs: {"m1": 0.81})

    df = pd.DataFrame({"review_text": ["good", "bad", ""]})
    out = csv_page._analyze_batch_reviews(df, "review_text", {"m1": object()}, True)

    assert len(out) == 3
    assert out[0]["Prediction"] == "Genuine"
    assert out[2]["Prediction"] == "N/A"


def test_analyze_amazon_reviews_feature(monkeypatch):
    _patch_streamlit_progress(monkeypatch, amazon_page)
    monkeypatch.setattr(
        amazon_page,
        "predict_review",
        lambda text, models, ensemble=True: (0, 0.66, {"m1": 0}, {"m1": 2.2}, 4.1),
    )
    monkeypatch.setattr(amazon_page, "_get_confidences", lambda *args, **kwargs: {"m1": 0.66})

    reviews = [{"username": "u1", "review": "not good", "stars": 2}]
    out = amazon_page._analyze_amazon_reviews(reviews, {"m1": object()}, True)

    assert len(out) == 1
    assert out[0]["Prediction"] == "Fake"
    assert out[0]["Username"] == "u1"


def test_analyze_walmart_reviews_feature(monkeypatch):
    _patch_streamlit_progress(monkeypatch, walmart_page)
    monkeypatch.setattr(
        walmart_page,
        "predict_review",
        lambda text, models, ensemble=True: (1, 0.72, {"m1": 1}, {"m1": 2.0}, 3.0),
    )
    monkeypatch.setattr(walmart_page, "_get_confidences", lambda *args, **kwargs: {"m1": 0.72})

    reviews = [
        {
            "author": "alice",
            "text": "works great",
            "rating": 5,
            "badges": ["Verified Purchase"],
        }
    ]
    out = walmart_page._analyze_walmart_reviews(reviews, {"m1": object()}, True)

    assert len(out) == 1
    assert out[0]["Prediction"] == "Genuine"
    assert out[0]["Verified_Purchase"] is True
