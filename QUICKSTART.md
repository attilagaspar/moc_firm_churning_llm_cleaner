# Quick Start Guide

## Setup (5 minutes)

### 1. Install Python Dependencies

Open terminal in the project folder and run:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure OpenAI API Key

1. Copy `.env.example` to `.env`:
   ```powershell
   copy .env.example .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-proj-...your_actual_key...
   ```

   Get your API key from: https://platform.openai.com/api-keys

### 3. Run the Application

```powershell
python main.py
```

## First Use

1. **Open Excel File**
   - Click "📂 Open File" button
   - Navigate to `example_data/` folder
   - Select your `.xls` or `.xlsx` file

2. **Process a Single Row**
   - Click on any row in the Excel viewer
   - Click "🔍 Lookup" button
   - Wait for LLM to process (5-15 seconds)
   - See results in JSON output panel below

3. **Batch Process**
   - Click on the starting row
   - Click "▶ Play" button
   - Confirm the batch operation
   - Click "⏹ Stop" anytime to pause

4. **Save Results**
   - File → Save Excel (creates timestamped XLSX in `output/` folder)
   - File → Save JSON (creates timestamped JSON in `output/` folder)

## Model Selection

Use the dropdown to choose:
- **gpt-4o-mini** (default, recommended) - Fast and cost-effective
- **gpt-4o** - More accurate, higher cost
- **gpt-4-turbo** - Balance of speed and accuracy
- **gpt-3.5-turbo** - Fastest, lowest cost, less accurate

## Tips

- Start with 1-2 rows to verify output quality
- GPT-4o-mini is usually sufficient for OCR cleaning
- The app auto-saves progress to the dataframe after each row
- Use Stop button to pause and save periodically during long runs
- Check `output/` folder for saved files

## Troubleshooting

**"LLM Error" on startup:**
- Verify `.env` file exists with valid OPENAI_API_KEY
- Check your OpenAI account has credits: https://platform.openai.com/usage

**Excel file won't load:**
- Ensure file format is `.xls` or `.xlsx`
- Try opening in Excel first to verify it's not corrupted

**Processing is slow:**
- API calls take 5-15 seconds per row
- This is normal for OpenAI API
- Consider using gpt-4o-mini for faster processing

**High costs:**
- Monitor usage: https://platform.openai.com/usage
- Expected cost: $0.001-0.003 per row with gpt-4o-mini
- Use gpt-3.5-turbo for even lower costs

## Expected Output Columns

After processing, you'll see these new columns:
- `cleaned_court` - Cleaned court name
- `cleaned_date` - Date in standard format
- `legal_identifier` - Extracted legal ID
- `cleaned_firm_name` - Fixed firm name
- `cleaned_location` - Fixed location
- `cleaned_owners` - Fixed owner names
- `cleaned_managers` - Fixed manager names
- `cleaned_notes_hu` - Cleaned Hungarian notes
- `notes_english` - English translation
- `event_classification` - Category 1-6
- `names_incoming` - People entering
- `names_outgoing` - People leaving
- `gazette_references` - References to other issues
- `model_used` - Which AI model was used
- `cleaning_date` - When it was processed

## Event Classifications

1. Firm birth (cégbejegyzés)
2. Firm death (cégtörlés)
3. Ownership change (tulajdonosváltozás)
4. Management change (vezetőváltozás)
5. Legal status change (jogi forma változás)
6. Other changes

---

**Need help?** Check the full README.md for detailed information.
