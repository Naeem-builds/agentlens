"""app_working.py - AgentLens that works without API key"""

import gradio as gr
import pandas as pd

# Sample LLM database for demonstration
LLM_DATABASE = [
    {
        "LLM Name": "GPT-4o",
        "Provider": "OpenAI",
        "Description": "OpenAI's flagship model with strong reasoning, multimodal capabilities, and robust function calling for complex agentic workflows",
        "Parameters": "200B+",
        "Key Features": "Native function calling, multimodal input, 128K context, JSON mode, parallel tool execution",
        "Tool/Function Calling Support": "✅ Yes - Full native support with parallel execution",
        "Cost Tier": "Medium-High",
        "Best For": "Complex multi-step agents, production deployments"
    },
    {
        "LLM Name": "Claude 3.5 Sonnet",
        "Provider": "Anthropic",
        "Description": "Excellent for coding agents and tasks requiring precise instruction following with 200K context window",
        "Parameters": "~175B",
        "Key Features": "Computer use beta, 200K context, strong coding, tool use, low hallucination",
        "Tool/Function Calling Support": "✅ Yes - Tool use beta available",
        "Cost Tier": "Medium",
        "Best For": "Coding assistants, document analysis agents"
    },
    {
        "LLM Name": "Llama 3.2 3B",
        "Provider": "Meta",
        "Description": "Lightweight open-weight model perfect for local deployment on consumer hardware",
        "Parameters": "3B",
        "Key Features": "Runs on 8GB RAM, good reasoning, efficient, open weights",
        "Tool/Function Calling Support": "✅ Yes - Native function calling",
        "Cost Tier": "Free (local)",
        "Best For": "Local development, privacy-focused agents"
    },
    {
        "LLM Name": "Mistral 7B",
        "Provider": "Mistral AI",
        "Description": "Balanced performance model with strong reasoning and function calling support",
        "Parameters": "7B",
        "Key Features": "Open weights, 32K context, good reasoning, Apache 2.0 license",
        "Tool/Function Calling Support": "✅ Yes",
        "Cost Tier": "Free (local)",
        "Best For": "General purpose local agents"
    },
    {
        "LLM Name": "Gemini 1.5 Pro",
        "Provider": "Google",
        "Description": "Massive 1M context window perfect for processing large documents and long conversations",
        "Parameters": "~175B",
        "Key Features": "1M context, multimodal, function calling, code execution",
        "Tool/Function Calling Support": "✅ Yes - Function calling with code execution",
        "Cost Tier": "Low-Medium",
        "Best For": "Long document processing, research agents"
    },
    {
        "LLM Name": "Qwen 2.5 7B",
        "Provider": "Alibaba",
        "Description": "Strong multilingual support with excellent tool use capabilities",
        "Parameters": "7B",
        "Key Features": "Multi-language, function calling, 128K context, strong math",
        "Tool/Function Calling Support": "✅ Yes",
        "Cost Tier": "Free (local)",
        "Best For": "Multilingual agents, math reasoning"
    }
]

def get_recommendations(query):
    """Filter recommendations based on query keywords"""
    query_lower = query.lower()
    
    # Simple keyword-based filtering
    if "customer" in query_lower or "support" in query_lower:
        filtered = [m for m in LLM_DATABASE if "GPT" in m["LLM Name"] or "Claude" in m["LLM Name"]]
    elif "coding" in query_lower or "code" in query_lower or "programming" in query_lower:
        filtered = [m for m in LLM_DATABASE if "Claude" in m["LLM Name"] or "Qwen" in m["LLM Name"]]
    elif "local" in query_lower or "privacy" in query_lower:
        filtered = [m for m in LLM_DATABASE if "Free" in m["Cost Tier"]]
    elif "cheap" in query_lower or "budget" in query_lower:
        filtered = [m for m in LLM_DATABASE if m["Cost Tier"] != "Medium-High"]
    else:
        filtered = LLM_DATABASE.copy()
    
    return filtered[:6]  # Return max 6 recommendations

def search_llms(query):
    """Main search function"""
    if not query:
        return "Please enter a query", pd.DataFrame()
    
    recommendations = get_recommendations(query)
    
    if not recommendations:
        return "No recommendations found. Try a different query.", pd.DataFrame()
    
    df = pd.DataFrame(recommendations)
    
    # Format markdown output
    markdown_output = f"## 🔍 Recommendations for: *{query}*\n\n"
    for i, model in enumerate(recommendations, 1):
        markdown_output += f"""
### {i}. **{model['LLM Name']}** *({model['Provider']})*

| Property | Value |
|----------|-------|
| **Description** | {model['Description']} |
| **Parameters** | {model['Parameters']} |
| **Tool Support** | {model['Tool/Function Calling Support']} |
| **Cost** | {model['Cost Tier']} |
| **Key Features** | {model['Key Features']} |

---
"""
    
    return markdown_output, df

# Create Gradio interface
with gr.Blocks(title="AgentLens - LLM Discovery Assistant", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🔍 AgentLens
    ### AI-Powered LLM Discovery Assistant for Agentic AI Workflows
    
    **No API key required!** This version uses a curated database of LLMs.
    """)
    
    gr.Markdown("""
    ### 📌 Example Queries to Try:
    - "I need a customer support agent that can handle tickets"
    - "Best LLM for a coding assistant with tool calling"
    - "What models can I run locally on my laptop?"
    - "Budget-friendly options for a marketing agent"
    """)
    
    with gr.Row():
        with gr.Column(scale=3):
            query_input = gr.Textbox(
                label="Describe your agentic workflow",
                placeholder="Example: I'm building a customer support agent that can answer tickets and escalate complex issues...",
                lines=4
            )
            search_btn = gr.Button("🔍 Search LLMs", variant="primary", size="lg")
    
    with gr.Tabs():
        with gr.TabItem("📋 Recommendations"):
            output_markdown = gr.Markdown("_Enter a query above to see recommendations_")
        with gr.TabItem("📊 Comparison Table"):
            output_table = gr.Dataframe(label="LLM Comparison", interactive=False)
    
    search_btn.click(
        fn=search_llms,
        inputs=query_input,
        outputs=[output_markdown, output_table]
    )
    
    gr.Markdown("""
    ---
    ### 💡 How It Works
    This version uses a pre-loaded database of LLMs. The full version would use:
    - **OpenAI Responses API** with real-time web search
    - **Ollama** for local model discovery
    - **Live model information** from the internet
    """)

if __name__ == "__main__":
    demo.launch(share=False)