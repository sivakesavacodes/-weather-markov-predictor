@echo off
title Markov Weather Predictor - Math Tests
cd /d "%~dp0"
echo ========================================================
echo   Running Mathematical Verification Tests...
echo ========================================================
python test_markov_model.py
echo.
pause
