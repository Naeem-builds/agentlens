"""
ollama_utils.py
---------------
Lists and manages locally installed Ollama models.
"""

import ollama
import re
from config import OLLAMA_BASE_URL


class OllamaManager:  # Note: Capital 'O' and 'M'
    """Manager for Ollama local models"""
    
    def __init__(self):
        try:
            self.client = ollama.Client(host=OLLAMA_BASE_URL) if OLLAMA_BASE_URL else ollama.Client()
        except:
            self.client = None
    
    def check_connection(self) -> bool:
        """Check if Ollama server is running"""
        if not self.client:
            return False
        try:
            self.client.list()
            return True
        except Exception:
            return False
    
    def list_models(self) -> list[dict]:
        """Get list of installed models with metadata"""
        if not self.client:
            return []
        try:
            response = self.client.list()
            models = []
            
            for m in response.models:
                name = m.model
                size_gb = round((m.size or 0) / 1e9, 1)
                
                models.append({
                    "name": name,
                    "size": f"{size_gb} GB",
                    "family": name.split(":")[0] if ":" in name else name,
                    "size_gb": size_gb,
                    "param_hint": self._extract_param_hint(name),
                    "tool_support": self._supports_tools(name),
                })
            
            return models
        except Exception:
            return []
    
    def check_model_suitability(self, model_name: str, query: str) -> bool:
        """Simple suitability check based on model capabilities"""
        capable_models = ["llama3", "mistral", "qwen2", "phi3", "command-r"]
        return any(cap in model_name.lower() for cap in capable_models)
    
    def test_model(self, model_name: str, prompt: str) -> str:
        """Test a local model with a prompt"""
        if not self.client:
            return "Ollama not connected"
        try:
            response = self.client.chat(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.message.content
        except Exception as e:
            return f"Error: {e}"
    
    def _extract_param_hint(self, model_name: str) -> str:
        """Extract parameter size from model name"""
        match = re.search(r"(\d+\.?\d*)\s*[bB]", model_name)
        if match:
            return f"{match.group(1)}B"
        return "Unknown"
    
    def _supports_tools(self, model_name: str) -> str:
        """Check if model likely supports tool calling"""
        tool_capable = [
            "llama3", "llama3.1", "llama3.2", "llama3.3",
            "mistral", "mixtral", "qwen2", "qwen2.5",
            "phi3", "phi4", "command-r",
        ]
        name_lower = model_name.lower()
        return "Yes" if any(t in name_lower for t in tool_capable) else "Limited"


# IMPORTANT: These are the functions your app_gradio.py is trying to import
# They need to match EXACTLY what you're importing
def get_local_models():  # Note: underscore, not camelCase
    """Convenience function - returns list of local models"""
    mgr = OllamaManager()
    return mgr.list_models()


def is_ollama_running():  # Note: underscore, not camelCase
    """Convenience function - check if Ollama is running"""
    mgr = OllamaManager()
    return mgr.check_connection()