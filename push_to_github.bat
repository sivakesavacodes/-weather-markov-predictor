@echo off
title Push Markov Weather Predictor to GitHub
cd /d "%~dp0"
echo ========================================================
echo   Pushing project to https://github.com/sivakesavacodes/weather-markov-predictor
echo ========================================================
echo.
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo   SUCCESS! All files uploaded to your GitHub!
    echo ========================================================
) else (
    echo ========================================================
    echo   If you saw an error, make sure you created the empty 
    echo   repository 'weather-markov-predictor' on github.com first!
    echo ========================================================
)
echo.
pause
