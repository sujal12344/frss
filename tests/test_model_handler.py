import pickle

import model_handler


def test_load_available_models_from_directory(tmp_path, monkeypatch):
    model_dir = tmp_path / "models"
    model_dir.mkdir()

    with open(model_dir / "LogisticRegression.pkl", "wb") as f:
        pickle.dump({"name": "lr"}, f)
    with open(model_dir / "models_summary.pkl", "wb") as f:
        pickle.dump({"summary": True}, f)

    monkeypatch.setattr(model_handler, "MODELS_DIR", str(model_dir))
    monkeypatch.setattr(model_handler.st, "error", lambda msg: None)
    monkeypatch.setattr(model_handler.st, "warning", lambda msg: None)

    loader = getattr(model_handler.load_available_models, "__wrapped__", model_handler.load_available_models)
    models = loader()

    assert "LogisticRegression" in models
    assert "models_summary" not in models


def test_load_available_models_missing_directory(monkeypatch):
    messages = []
    monkeypatch.setattr(model_handler, "MODELS_DIR", "Z:/missing_models_dir")
    monkeypatch.setattr(model_handler.st, "error", lambda msg: messages.append(msg))

    loader = getattr(model_handler.load_available_models, "__wrapped__", model_handler.load_available_models)
    models = loader()

    assert models == {}
    assert any("not found" in m for m in messages)


def test_load_model_metrics(tmp_path, monkeypatch):
    model_dir = tmp_path / "models"
    model_dir.mkdir()
    metrics_data = {"m1": {"accuracy": 0.91}}

    with open(model_dir / "models_summary.pkl", "wb") as f:
        pickle.dump(metrics_data, f)

    monkeypatch.setattr(model_handler, "MODELS_DIR", str(model_dir))
    monkeypatch.setattr(model_handler.st, "warning", lambda msg: None)

    loader = getattr(model_handler.load_model_metrics, "__wrapped__", model_handler.load_model_metrics)
    metrics = loader()
    assert metrics == metrics_data


def test_get_model_metric_defaults():
    metrics = {"m1": {"accuracy": 0.95}}
    assert model_handler.get_model_metric(metrics, "m1", "accuracy") == 0.95
    assert model_handler.get_model_metric(metrics, "m1", "precision", "N/A") == "N/A"
    assert model_handler.get_model_metric(metrics, "missing", "accuracy", "N/A") == "N/A"
