@echo off
REM Run script for Hungarian Firm Registry LLM Cleaner
REM This activates the virtual environment and runs the application

echo Starting Hungarian Firm Registry LLM Cleaner...
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to install dependencies.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your OpenAI API key.
    echo.
    pause
)

REM Activate virtual environment and run
call venv\Scripts\activate.bat
python main.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)
