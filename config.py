"""config.py - Settings and constants for AgentLens"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"  # Good balance of cost/performance
MAX_RECOMMENDATIONS = 6

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"

# Error messages
API_KEY_MISSING_MSG = """
❌ OpenAI API key not found!

1. Create a .env file in the project root
2. Add your API key: OPENAI_API_KEY=sk-...
3. Get a key from https://platform.openai.com/api-keys
"""