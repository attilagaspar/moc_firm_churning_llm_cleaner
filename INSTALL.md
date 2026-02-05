# Installation Instructions

## Windows Quick Install (Easiest Method)

### 1. Double-click `setup.bat`
This will automatically:
- Check for Python installation
- Create a virtual environment
- Install all dependencies
- Create .env file from template

### 2. Edit `.env` file
- Open `.env` in Notepad
- Replace `your_api_key_here` with your OpenAI API key
- Get key from: https://platform.openai.com/api-keys
- Save and close

### 3. Double-click `run.bat`
- This launches the application
- GUI window will open
- Start processing your data!

---

## Manual Installation (Alternative Method)

### Step 1: Install Python
If not already installed:
- Download Python 3.8+ from https://www.python.org/downloads/
- ✅ Check "Add Python to PATH" during installation
- Verify: Open cmd and type `python --version`

### Step 2: Open Command Prompt in Project Folder
- Hold Shift, right-click in folder → "Open PowerShell window here"
- Or: Open cmd, navigate with `cd` command

### Step 3: Create Virtual Environment
```cmd
python -m venv venv
```

### Step 4: Activate Virtual Environment
```cmd
venv\Scripts\activate
```
You should see `(venv)` at the beginning of your command prompt.

### Step 5: Install Dependencies
```cmd
pip install -r requirements.txt
```
This installs:
- pandas (Excel processing)
- openpyxl (Excel I/O)
- openai (LLM API)
- python-dotenv (configuration)

### Step 6: Setup API Key
```cmd
copy .env.example .env
```
Then edit `.env` in Notepad:
```
OPENAI_API_KEY=sk-proj-YOUR_ACTUAL_KEY_HERE
```

### Step 7: Run Application
```cmd
python main.py
```

---

## Troubleshooting Installation

### "Python is not recognized..."
**Problem**: Python not in PATH
**Solution**: 
- Reinstall Python, check "Add Python to PATH"
- Or manually add Python to PATH in System Environment Variables

### "pip is not recognized..."
**Problem**: pip not installed
**Solution**:
```cmd
python -m ensurepip --upgrade
```

### "No module named 'tkinter'"
**Problem**: tkinter not included (rare on Windows)
**Solution**: 
- On Windows: Usually included with Python
- Reinstall Python from python.org (official installer includes tkinter)

### "Failed to install dependencies"
**Problem**: Network issues or pip outdated
**Solution**:
```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### "Permission denied" errors
**Problem**: Admin rights needed
**Solution**:
- Run cmd as Administrator
- Or use `--user` flag: `pip install --user -r requirements.txt`

### Virtual environment issues
**Problem**: Can't activate venv
**Solution**:
```cmd
# Delete old venv
rmdir /s venv

# Create new one
python -m venv venv

# Try activating again
venv\Scripts\activate
```

---

## Verifying Installation

After installation, verify everything works:

### 1. Check Python packages
```cmd
pip list
```
Should show:
- pandas
- openpyxl
- openai
- python-dotenv

### 2. Test imports
```cmd
python -c "import pandas, openpyxl, openai, dotenv, tkinter; print('All imports successful!')"
```

### 3. Check API key
```cmd
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key loaded:', 'sk-' in str(os.getenv('OPENAI_API_KEY')))"
```

Should print: `API Key loaded: True`

---

## First Run Checklist

Before using the application:

- ✅ Python 3.8+ installed
- ✅ All dependencies installed (`pip list` shows them)
- ✅ `.env` file exists with valid API key
- ✅ `example_data/` folder has Excel file
- ✅ Virtual environment activated (if using manual method)

---

## Updating the Application

To update dependencies:
```cmd
pip install --upgrade -r requirements.txt
```

To update OpenAI package specifically:
```cmd
pip install --upgrade openai
```

---

## Uninstalling

To completely remove:
1. Delete the entire project folder
2. That's it! Virtual environment is self-contained

To keep project but remove virtual environment:
```cmd
rmdir /s venv
```
Then run setup.bat again when needed.

---

## Getting Help

If you encounter issues:

1. **Check OpenAI Account**
   - Visit: https://platform.openai.com/usage
   - Verify you have credits
   - Check API key is active

2. **Check Example Data**
   - Ensure Excel file has 9 columns
   - File opens in Excel without errors

3. **Check Error Messages**
   - Application shows detailed error messages
   - JSON output panel shows API errors

4. **Read Documentation**
   - README.md - Full documentation
   - QUICKSTART.md - Quick guide
   - WORKFLOW.md - Architecture details

---

## System Requirements

**Minimum:**
- Windows 10 or later
- Python 3.8+
- 4 GB RAM
- Internet connection
- OpenAI API account

**Recommended:**
- Windows 10/11
- Python 3.10+
- 8 GB RAM
- Stable internet
- OpenAI API account with credits

**Disk Space:**
- Project files: ~2 MB
- Virtual environment: ~50 MB
- Dependencies: ~200 MB
- Total: ~250 MB

---

**Installation Complete! Now read QUICKSTART.md to start using the application.**
