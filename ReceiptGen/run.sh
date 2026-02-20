#!/bin/bash
source venv/bin/activate
echo "Starting Ollama..."
ollama serve > /dev/null 2>&1 & 
sleep 5
echo "Launching Receipt App..."
streamlit run app.py
