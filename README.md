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

3. Register the project kernel:

   ```bash
   uv run python -m ipykernel install --user --name genai-search-with-duckduckgo-and-tavily --display-name "Python (genai-search-with-duckduckgo-and-tavily)"
   ```

4. Start JupyterLab with uv:

   ```bash
   uv run jupyter lab
   ```

5. Open `notebook.ipynb` and select the `Python (genai-search-with-duckduckgo-and-tavily)` kernel if prompted.

## Test

```bash
uv run pytest
```
