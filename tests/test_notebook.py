import importlib.util
from pathlib import Path

import pytest
from duckduckgo_search.exceptions import DuckDuckGoSearchException


MODULE_PATH = Path(__file__).resolve().parent.parent / "search_tools.py"


def load_search_tools():
    spec = importlib.util.spec_from_file_location("search_tools", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_search_uses_duckduckgo_results(monkeypatch):
    search_tools = load_search_tools()

    class FakeDDGS:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def text(self, query, max_results):
            assert query == "hello"
            assert max_results == 2
            return [{"title": "duckduckgo"}]

    monkeypatch.setattr(search_tools, "DDGS", FakeDDGS)

    result = search_tools.search("hello", max_results=2)

    assert result == {
        "provider": "duckduckgo",
        "results": [{"title": "duckduckgo"}],
    }


def test_search_falls_back_to_tavily(monkeypatch):
    search_tools = load_search_tools()

    class FailingDDGS:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def text(self, query, max_results):
            raise DuckDuckGoSearchException("duckduckgo unavailable")

    class FakeTavilyClient:
        def __init__(self, api_key):
            assert api_key == "test-key"

        def search(self, query, max_results):
            assert query == "hello"
            assert max_results == 2
            return {"results": [{"title": "tavily"}]}

    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    monkeypatch.setattr(search_tools, "DDGS", FailingDDGS)
    monkeypatch.setattr(search_tools, "TavilyClient", FakeTavilyClient)

    result = search_tools.search("hello", max_results=2)

    assert result == {
        "provider": "tavily",
        "results": [{"title": "tavily"}],
        "duckduckgo_error": "duckduckgo unavailable",
    }


def test_search_raises_when_fallback_is_unavailable(monkeypatch):
    search_tools = load_search_tools()

    class FailingDDGS:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def text(self, query, max_results):
            raise DuckDuckGoSearchException("duckduckgo unavailable")

    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    monkeypatch.setattr(search_tools, "DDGS", FailingDDGS)

    with pytest.raises(
        RuntimeError,
        match="DuckDuckGo search failed and no Tavily API key is configured.",
    ):
        search_tools.search("hello")
