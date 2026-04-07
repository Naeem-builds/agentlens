"""
agent_core.py
-------------
Core AI engine for AgentLens.
Uses the OpenAI Responses API with the built-in web_search tool.
"""

import json
import re
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, MAX_RECOMMENDATIONS, API_KEY_MISSING_MSG


SYSTEM_PROMPT = f"""
You are AgentLens, an expert assistant that recommends LLMs for agentic AI workflows.

When a user describes their workflow, you must:
1. Use web_search to find current LLM information
2. Return EXACTLY {MAX_RECOMMENDATIONS} recommendations as a JSON array
3. Use these EXACT field names (this is CRITICAL):

{{
  "LLM Name": "Official model name",
  "Description": "1-2 sentence summary for this use case", 
  "Parameters": "Model size (e.g., 7B, 70B, 405B)",
  "Key Features": "Bullet list as a single string with commas or newlines",
  "Tool/Function Calling Support": "Yes or No with details"
}}

Return ONLY the JSON array. No markdown, no extra text.
"""


class AgentLensCore:
    """Main engine for LLM discovery"""
    
    def __init__(self):
        self.client = None
        if OPENAI_API_KEY:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def test_connection(self) -> bool:
        """Test if OpenAI API is working"""
        return self.client is not None
    
    def get_llm_recommendations(self, user_query: str) -> list[dict]:
        """Get LLM recommendations for a workflow description"""
        
        if not self.client:
            raise ValueError(API_KEY_MISSING_MSG)
        
        try:
            response = self.client.responses.create(
                model=OPENAI_MODEL,
                tools=[{"type": "web_search_preview"}],
                instructions=SYSTEM_PROMPT,
                input=user_query,
            )
            
            # Extract text from response
            raw_text = ""
            for item in response.output:
                if hasattr(item, "content"):
                    for block in item.content:
                        if hasattr(block, "text"):
                            raw_text += block.text
            
            if not raw_text.strip():
                return []
            
            return self._parse_json_response(raw_text)
            
        except Exception as e:
            print(f"[AgentLens] Error: {e}")
            return []
    
    def _parse_json_response(self, raw_text: str) -> list[dict]:
        """Safely parse JSON from model response"""
        # Remove markdown fences
        cleaned = re.sub(r"```(?:json)?", "", raw_text).strip().rstrip("`").strip()
        
        # Find JSON array
        match = re.search(r"\[.*\]", cleaned, re.DOTALL)
        if match:
            cleaned = match.group(0)
        
        try:
            data = json.loads(cleaned)
            if isinstance(data, list):
                return data
        except json.JSONDecodeError as e:
            print(f"[AgentLens] JSON parse error: {e}")
        
        return []