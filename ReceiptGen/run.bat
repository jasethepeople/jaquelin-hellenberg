@echo off
echo Starting Ollama and Receipt App...
start /b ollama serve
timeout /t 5 > nul
streamlit run app.py
pause
