@echo off
title Markov Weather Predictor
cd /d "%~dp0"
echo ========================================================
echo   Starting MARKOV WEATHER PREDICTOR Dashboard...
echo ========================================================
python -m streamlit run app.py
pause
