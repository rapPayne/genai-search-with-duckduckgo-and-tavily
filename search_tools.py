import os

from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException
from tavily import TavilyClient


def search_duckduckgo(query: str, max_results: int = 5) -> list[dict]:
    with DDGS() as ddgs:
        return list(ddgs.text(query, max_results=max_results))


def search_tavily(query: str, max_results: int = 5) -> list[dict]:
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("Set TAVILY_API_KEY to enable the Tavily fallback.")

    client = TavilyClient(api_key=api_key)
    response = client.search(query=query, max_results=max_results)
    return response.get("results", [])


def search(query: str, max_results: int = 5) -> dict:
    try:
        return {
            "provider": "duckduckgo",
            "results": search_duckduckgo(query=query, max_results=max_results),
        }
    except DuckDuckGoSearchException as duckduckgo_error:
        if not os.environ.get("TAVILY_API_KEY"):
            raise RuntimeError(
                "DuckDuckGo search failed and no Tavily API key is configured."
            ) from duckduckgo_error

        return {
            "provider": "tavily",
            "results": search_tavily(query=query, max_results=max_results),
            "duckduckgo_error": str(duckduckgo_error),
        }
