# Hungarian Firm Registry LLM Data Cleaner

An LLM-powered data cleaning tool for historical Hungarian firm registry data from "Központi Értesítő" (Central Gazette of the Ministry of Commerce) from the turn of the 19th-20th century.

## Overview

This tool uses OpenAI's language models to:
- Clean OCR errors from scanned historical documents
- Extract and structure firm information
- Recognize entities (locations, firm names, personal names)
- Classify registry events (firm birth, death, ownership changes, etc.)
- Translate Hungarian notes to English

## Features

- **GUI Interface**: Easy-to-use interface with Excel viewer and JSON output display
- **Auto-Save**: Progress saved after each row - resume anytime from where you left off
- **Batch Processing**: Process individual rows or automatically process from selected row onwards
- **Model Selection**: Choose from various OpenAI models (default: GPT-4o-mini)
- **Dual Output**: Enhanced XLSX file + JSON export
- **Entity Recognition**: Automatically extract names, locations, and dates
- **Event Classification**: Classify registry events into 6 categories

## Installation

1. **Clone the repository** (or navigate to the project folder)

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API key**:
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Starting the Application

```bash
python main.py
```

### GUI Components

1. **Excel Viewer** (Upper panel):
   - Displays the input Excel file
   - Select rows to process
   - Shows original OCR data

2. **JSON Output** (Lower panel):
   - Displays LLM response in JSON format
   - Shows structured extracted data

3. **Controls**:
   - **File → Open**: Load an Excel file
   - **File → Save**: Save cleaned data
   - **Model Dropdown**: Select OpenAI model (gpt-4o-mini, gpt-4o, gpt-4-turbo, gpt-3.5-turbo)
   - **Lookup Button**: Process selected row
   - **Play Button**: Auto-process from selected row onwards
   - **Stop Button**: Stop auto-processing

### Input Data Structure

Expected Excel columns (in order):
1. Court registration location
2. Date and legal identifier
3. Firm name
4. Main location of firm
5. Owner (Czég birtokosa)
6. Managers (Czégvezetők)
7. [Ignored column - badly scanned vertical text]
8. Notes (most important - contains event details)
9. Source filename

### Output Data

The tool adds the following columns to the Excel file:
- `cleaned_court`: Cleaned court field
- `cleaned_date`: Cleaned date
- `legal_identifier`: Extracted legal identifier
- `cleaned_firm_name`: Cleaned firm name
- `cleaned_location`: Cleaned main location
- `cleaned_owners`: Cleaned owner names
- `cleaned_managers`: Cleaned manager names
- `cleaned_notes_hu`: Cleaned Hungarian notes
- `notes_english`: English translation/summary
- `event_classification`: Event type (1-6)
- `names_incoming`: Names entering management/ownership
- `names_outgoing`: Names leaving management/ownership
- `gazette_references`: References to other gazette issues
- `model_used`: OpenAI model used for cleaning
- `cleaning_date`: Timestamp of cleaning

### Event Classification

- **1**: Firm birth (registration)
- **2**: Firm death (dissolution)
- **3**: Ownership change
- **4**: Management change
- **5**: Change in legal status (e.g., kft. → rt.)
- **6**: Other changes

## Project Structure

```
moc_firm_churning_llm_cleaner/
├── example_data/          # Input Excel files
├── output/                # Generated output files
├── prompt/                # Prompt templates
├── src/
│   ├── config.py         # Configuration and prompts
│   ├── data_handler.py   # Excel and JSON I/O
│   └── llm_processor.py  # LLM API interaction
├── main.py               # Main GUI application
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
```

## API Costs

Using GPT-4o-mini (recommended for this task) is cost-effective:
- Approximate cost: $0.15 per 1M input tokens, $0.60 per 1M output tokens
- Expected cost per row: ~$0.001-0.003

For large datasets, monitor your OpenAI usage at: https://platform.openai.com/usage

## Notes

- **Auto-Save**: The app automatically saves progress after each row to `output/[filename]_cleaned.xlsx`. If interrupted, simply reopen the same input file to resume from where you left off. See [AUTO_SAVE.md](AUTO_SAVE.md) for details.
- The tool handles the Hungarian "macskaköröm" (") symbol, which indicates "same as above"
- Layout errors like "P o z s o n y" are automatically corrected to "Pozsony"
- The tool creates an `output/` directory for processed files

## Troubleshooting

**Import Error: No module named 'tkinter'**
- On Windows: tkinter comes with Python
- On Linux: `sudo apt-get install python3-tk`
- On Mac: tkinter comes with Python

**OpenAI API Error**
- Check your API key in `.env` file
- Verify your OpenAI account has credits
- Check internet connection

**Excel File Not Loading**
- Ensure file is in `.xls` or `.xlsx` format
- Check for file corruption
- Try opening in Excel to verify

## License

This tool is for research purposes.

## Contact

For questions or issues, please contact the project maintainer.
