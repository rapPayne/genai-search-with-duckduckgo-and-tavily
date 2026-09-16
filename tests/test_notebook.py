import json
from pathlib import Path

import pytest
from duckduckgo_search.exceptions import DuckDuckGoSearchException


NOTEBOOK_PATH = Path(__file__).resolve().parent.parent / "notebook.ipynb"


def load_notebook_namespace():
    notebook = json.loads(NOTEBOOK_PATH.read_text())
    namespace = {}

    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue

        source = "".join(cell["source"])
        if "result = search(query)" in source or "pprint(result[" in source:
            continue

        exec(compile(source, "notebook.ipynb", "exec"), namespace)

    return namespace


def test_search_uses_duckduckgo_results():
    namespace = load_notebook_namespace()

    class FakeDDGS:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def text(self, query, max_results):
            assert query == "hello"
            assert max_results == 2
            return [{"title": "duckduckgo"}]

    namespace["DDGS"] = FakeDDGS

    result = namespace["search"]("hello", max_results=2)

    assert result == {
        "provider": "duckduckgo",
        "results": [{"title": "duckduckgo"}],
    }


def test_search_falls_back_to_tavily(monkeypatch):
    namespace = load_notebook_namespace()

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
    namespace["DDGS"] = FailingDDGS
    namespace["TavilyClient"] = FakeTavilyClient

    result = namespace["search"]("hello", max_results=2)

    assert result == {
        "provider": "tavily",
        "results": [{"title": "tavily"}],
        "duckduckgo_error": "duckduckgo unavailable",
    }


def test_search_raises_when_fallback_is_unavailable(monkeypatch):
    namespace = load_notebook_namespace()

    class FailingDDGS:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def text(self, query, max_results):
            raise DuckDuckGoSearchException("duckduckgo unavailable")

    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    namespace["DDGS"] = FailingDDGS

    with pytest.raises(
        RuntimeError,
        match="DuckDuckGo search failed and no Tavily API key is configured.",
    ):
        namespace["search"]("hello")
