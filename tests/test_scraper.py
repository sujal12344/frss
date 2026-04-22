from contextlib import contextmanager

import scraper


class FakeResponse:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text

    def json(self):
        return self._payload


@contextmanager
def no_op_spinner(_text):
    yield


def test_fetch_amazon_reviews_success(monkeypatch):
    monkeypatch.setattr(scraper.st, "spinner", no_op_spinner)
    monkeypatch.setattr(scraper.st, "error", lambda msg: None)
    monkeypatch.setattr(
        scraper.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(200, {"reviews": [{"review": "ok"}]}),
    )

    result = scraper.fetch_amazon_reviews("B07FTKQ97Q")
    assert result is not None
    assert "reviews" in result


def test_fetch_amazon_reviews_not_found(monkeypatch):
    errors = []
    monkeypatch.setattr(scraper.st, "spinner", no_op_spinner)
    monkeypatch.setattr(scraper.st, "error", lambda msg: errors.append(msg))
    monkeypatch.setattr(scraper.requests, "get", lambda *args, **kwargs: FakeResponse(404))

    result = scraper.fetch_amazon_reviews("INVALID")
    assert result is None
    assert any("Product not found" in m for m in errors)


def test_fetch_amazon_reviews_exception(monkeypatch):
    errors = []
    monkeypatch.setattr(scraper.st, "spinner", no_op_spinner)
    monkeypatch.setattr(scraper.st, "error", lambda msg: errors.append(msg))

    def raise_error(*args, **kwargs):
        raise TimeoutError("network timeout")

    monkeypatch.setattr(scraper.requests, "get", raise_error)
    result = scraper.fetch_amazon_reviews("B07FTKQ97Q")
    assert result is None
    assert any("Error fetching data" in m for m in errors)


def test_fetch_walmart_reviews_success(monkeypatch):
    monkeypatch.setattr(scraper.st, "spinner", no_op_spinner)
    monkeypatch.setattr(scraper.st, "error", lambda msg: None)
    monkeypatch.setattr(
        scraper.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(200, {"reviews": [{"text": "great"}]}),
    )

    result = scraper.fetch_walmart_reviews("123456")
    assert result is not None
    assert "reviews" in result


def test_fetch_walmart_reviews_api_error(monkeypatch):
    errors = []
    monkeypatch.setattr(scraper.st, "spinner", no_op_spinner)
    monkeypatch.setattr(scraper.st, "error", lambda msg: errors.append(msg))
    monkeypatch.setattr(
        scraper.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(500, text="server error"),
    )

    result = scraper.fetch_walmart_reviews("123456")
    assert result is None
    assert any("API Error" in m for m in errors)
