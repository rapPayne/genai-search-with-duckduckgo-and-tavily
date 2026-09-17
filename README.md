# genai-search-with-duckduckgo-and-tavily

Jupyter notebook running an LLM (via [OpenRouter](https://openrouter.ai), through [LangChain](https://python.langchain.com)) with a `search` tool. The model decides when to search; the tool itself searches DuckDuckGo (free) with Tavily as a fallback.

By default the notebook uses `anthropic/claude-haiku-4.5` as the model — change the `MODEL` variable in `notebook.ipynb` to use a different OpenRouter model.

## Run with uv

1. Create the environment and install dependencies:

   ```bash
   uv sync --dev
   ```

2. Copy `.env.example` to `.env` and fill in your API keys:

   ```bash
   cp .env.example .env
   ```

   - `OPENROUTER_API_KEY` — required, used for inference.
   - `TAVILY_API_KEY` — optional, used only as a fallback when DuckDuckGo fails.

3. Register the project kernel:

   ```bash
   uv run python -m ipykernel install --user --name genai-search-with-duckduckgo-and-tavily --display-name "Python (genai-search-with-duckduckgo-and-tavily)"
   ```

4. Start JupyterLab with uv:

   ```bash
   uv run jupyter lab
   ```

5. Open `notebook.ipynb` and select the `Python (genai-search-with-duckduckgo-and-tavily)` kernel if prompted.
