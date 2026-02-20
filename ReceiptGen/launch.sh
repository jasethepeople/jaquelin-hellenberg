#!/bin/bash
echo "--- Initializing Environment ---"
source venv/bin/activate
pip install streamlit ollama fpdf pillow -q
echo "--- Starting Application ---"
streamlit run app.py
