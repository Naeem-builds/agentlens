@echo off
echo ========================================
echo AgentLens - Optimized for 8GB RAM
echo ========================================

echo.
echo Step 1: Starting Ollama (lightweight mode)...
start /B ollama serve > nul 2>&1
timeout /t 3 /nobreak > nul

echo Step 2: Checking RAM usage...
wmic OS get TotalVisibleMemorySize,FreePhysicalMemory

echo.
echo Step 3: Starting AgentLens...
echo If Gradio is slow, press Ctrl+C and run: uv run python app_gradio.py

pause