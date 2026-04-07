<<<<<<< HEAD
# AgentLens 🔍

AI-Powered LLM Discovery Assistant for Agentic AI Workflows

## What it does
AgentLens accepts a natural language description of an agentic AI workflow and recommends the best LLMs using:
- **OpenAI Responses API** with real-time web search
- **Ollama** for local open-source model discovery
- **Streamlit** for an interactive web UI

## Setup

### 1. Install uv (if you haven't)
```bash
# Windows PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Mac / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and install dependencies
```bash
git clone <your-repo-url>
cd agentlens
uv sync
```

### 3. Add your OpenAI API key
Create a `.env` file:
```
OPENAI_API_KEY=your_key_here
```

### 4. Install and start Ollama (optional but recommended)
Download from https://ollama.com then:
```bash
ollama serve
ollama pull llama3.2
ollama pull mistral
ollama pull qwen2.5
```

### 5. Run the app
```bash
uv run streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Example queries
- "I'm building a marketing automation agent — recommend LLMs"
- "Best models for a customer support agentic workflow with tool calling"
- "Which LLMs support function calling for a coding agent?"

## Project structure
```
agentlens/
├── app.py           # Streamlit UI
├── agent_core.py    # OpenAI Responses API + web search logic
├── ollama_utils.py  # Local Ollama model utilities
├── config.py        # Settings and constants
├── .env             # API keys (never commit this!)
├── pyproject.toml   # uv project file
└── README.md
```

## Tech stack
| Component | Technology |
|-----------|-----------|
| AI Engine | OpenAI Responses API with web_search_preview tool |
| Local models | Ollama |
| UI | Streamlit |
| Data | Pandas |
| Config | python-dotenv |
| Package manager | uv |
=======
# agentlens
to check which llm is best for user
>>>>>>> eea91feaf8e6bbe3ed1e6b2312a20601ef779cf3
