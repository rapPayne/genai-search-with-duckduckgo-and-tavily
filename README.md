# genai-search-with-duckduckgo-and-tavily

Jupyter notebook demonstrating how to provide an LLM with a tool that searches using DuckDuckGo (free) with Tavily as a fallback.

## Run with uv

1. Create the environment and install dependencies:

   ```bash
   uv sync --dev
   ```

2. Optionally export a Tavily API key for fallback searches:

   ```bash
   export TAVILY_API_KEY=your-key-here
   ```

3. Start JupyterLab with uv:

   ```bash
   uv run jupyter lab
   ```

4. Open `notebook.ipynb`.

## Test

```bash
uv run pytest
```
