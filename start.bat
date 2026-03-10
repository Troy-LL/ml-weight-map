@echo off
title Prompteering MVP
echo.
echo   Prompteering MVP — Starting...
echo.

if not exist "venv" (
    echo   Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

echo   Installing dependencies...
pip install -r requirements.txt --quiet

echo   Launching server...
echo.
python server.py

pause
