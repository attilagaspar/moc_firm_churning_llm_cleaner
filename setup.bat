@echo off
REM Setup script for Hungarian Firm Registry LLM Cleaner
REM Run this script to set up the project automatically

echo ========================================
echo Hungarian Firm Registry LLM Cleaner
echo Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [1/4] Python found:
python --version
echo.

REM Create virtual environment
echo [2/4] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
)
echo.

REM Activate virtual environment and install dependencies
echo [3/4] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Setup .env file
echo [4/4] Setting up .env file...
if exist .env (
    echo .env file already exists, skipping...
) else (
    copy .env.example .env
    echo .env file created from template
    echo.
    echo IMPORTANT: Please edit .env and add your OpenAI API key!
    echo    1. Open .env in a text editor
    echo    2. Replace 'your_api_key_here' with your actual API key
    echo    3. Get API key from: https://platform.openai.com/api-keys
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Edit .env file and add your OpenAI API key
echo   2. Run: run.bat
echo      or: venv\Scripts\activate.bat
echo      and: python main.py
echo.
echo Read QUICKSTART.md for detailed instructions.
echo.
pause
