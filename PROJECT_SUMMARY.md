# Project Structure and Files

## Complete Package Overview

```
moc_firm_churning_llm_cleaner/
│
├── main.py                    # Main GUI application (entry point)
├── requirements.txt           # Python dependencies
├── README.md                  # Full documentation
├── QUICKSTART.md             # Quick start guide
├── .gitignore                # Git ignore rules
├── .env.example              # Environment variable template
│
├── src/                      # Source code package
│   ├── __init__.py          # Package initializer
│   ├── config.py            # Configuration and prompts
│   ├── llm_processor.py     # OpenAI API integration
│   └── data_handler.py      # Excel/JSON file operations
│
├── example_data/             # Input Excel files location
│   └── [Your .xls/.xlsx files go here]
│
├── output/                   # Generated output files
│   ├── [Cleaned .xlsx files]
│   └── [Cleaned .json files]
│
└── prompt/                   # Prompt documentation
    └── README.md            # Prompt customization guide
```

## File Descriptions

### Core Application Files

- **main.py** (31KB)
  - Complete GUI application using tkinter
  - Excel viewer with row selection
  - JSON output display
  - Play/Stop/Lookup controls
  - Model selection dropdown
  - Threading for responsive UI
  - Auto-save functionality

- **src/llm_processor.py** (5KB)
  - OpenAI API client wrapper
  - Row data processing
  - Structured JSON output using OpenAI's schema
  - Error handling and retries
  - Model switching capability

- **src/data_handler.py** (5KB)
  - Excel file I/O (both .xls and .xlsx)
  - JSON export functionality
  - DataFrame management
  - Output column initialization
  - Timestamp-based file naming

- **src/config.py** (5KB)
  - Model options and defaults
  - Column name mappings
  - Event classification definitions
  - System and user prompt templates
  - JSON schema for structured outputs

### Documentation Files

- **README.md**
  - Complete project documentation
  - Installation instructions
  - Feature overview
  - Usage guide
  - Troubleshooting

- **QUICKSTART.md**
  - 5-minute setup guide
  - First-use walkthrough
  - Common tips and tricks
  - Quick troubleshooting

- **prompt/README.md**
  - Prompt customization guide
  - Hungarian language notes
  - OCR error patterns
  - Best practices

### Configuration Files

- **requirements.txt**
  - Python package dependencies
  - Pinned versions for stability
  - Core: pandas, openpyxl, openai, python-dotenv

- **.env.example**
  - Template for environment variables
  - Copy to .env and add your API key

- **.gitignore**
  - Excludes sensitive files (API keys)
  - Excludes output files
  - Includes example_data

## Key Features Implemented

### ✅ GUI Components
- [x] Tkinter-based interface
- [x] Excel data viewer (Treeview widget)
- [x] JSON output display (ScrolledText)
- [x] Model selection dropdown
- [x] Lookup button (single row processing)
- [x] Play button (batch processing)
- [x] Stop button (interrupt processing)
- [x] Status bar with real-time updates
- [x] Menu bar (File, Help)

### ✅ Data Processing
- [x] Excel file loading (.xls and .xlsx)
- [x] Row selection and processing
- [x] OpenAI API integration
- [x] Structured JSON output
- [x] OCR error cleaning
- [x] Entity recognition
- [x] Event classification (1-6)
- [x] Hungarian to English translation
- [x] Name extraction (incoming/outgoing)
- [x] Gazette reference extraction

### ✅ Output Generation
- [x] New columns added to Excel
- [x] Timestamped output files
- [x] JSON export with full data
- [x] Metadata tracking (model, date)
- [x] Progress saving (row-by-row)

### ✅ User Experience
- [x] Threading for responsive UI
- [x] Progress indicators
- [x] Error handling with user feedback
- [x] Confirmation dialogs
- [x] Auto-scroll to current row
- [x] Stop/resume capability
- [x] Multiple model options

### ✅ Documentation
- [x] Comprehensive README
- [x] Quick start guide
- [x] Code comments
- [x] Prompt customization guide
- [x] API setup instructions

## Technology Stack

- **Language**: Python 3.8+
- **GUI Framework**: tkinter (built-in)
- **Data Processing**: pandas, openpyxl
- **LLM API**: OpenAI Python SDK
- **Configuration**: python-dotenv
- **Threading**: Python threading module

## Input Data Format

Expected Excel columns (in order):
1. Court registration location
2. Date and legal identifier
3. Firm name
4. Main location
5. Owner (Czég birtokosa)
6. Managers (Czégvezetők)
7. [Ignored - bad scan column]
8. Notes (critical - event details)
9. Source filename

## Output Data Format

15 new columns added:
1. `cleaned_court` - Cleaned court field
2. `cleaned_date` - Standardized date (YYYY.MM.DD.)
3. `legal_identifier` - Extracted legal ID
4. `cleaned_firm_name` - OCR-corrected firm name
5. `cleaned_location` - OCR-corrected location
6. `cleaned_owners` - Cleaned owner names
7. `cleaned_managers` - Cleaned manager names
8. `cleaned_notes_hu` - Cleaned Hungarian text
9. `notes_english` - English summary
10. `event_classification` - Event type (1-6)
11. `names_incoming` - Names entering firm
12. `names_outgoing` - Names leaving firm
13. `gazette_references` - Other gazette references
14. `model_used` - OpenAI model used
15. `cleaning_date` - Processing timestamp

## Next Steps for Users

1. **Setup**: Follow QUICKSTART.md
2. **Test**: Process 1-2 sample rows
3. **Verify**: Check output quality
4. **Adjust**: Modify prompts if needed (see prompt/README.md)
5. **Batch**: Process full dataset
6. **Export**: Save to Excel and JSON

## Cost Estimation

With **gpt-4o-mini** (recommended):
- Input: ~500 tokens/row × $0.15/1M tokens = $0.000075/row
- Output: ~800 tokens/row × $0.60/1M tokens = $0.000480/row
- **Total: ~$0.00055/row** or **$0.55 per 1000 rows**

For a 10,000 row dataset: approximately **$5-6 USD**

## Support and Customization

All code is well-commented and modular. Key customization points:

1. **Prompts**: Edit `src/config.py`
2. **Output columns**: Modify `OUTPUT_COLUMNS` in `src/config.py`
3. **Event classifications**: Update `EVENT_TYPES` in `src/config.py`
4. **Model parameters**: Adjust in `src/llm_processor.py` (temperature, etc.)
5. **GUI layout**: Modify `main.py` _setup_gui() method

## Known Limitations

- Processing speed limited by API rate limits (~60 rows/minute)
- Requires active internet connection
- Cost scales linearly with dataset size
- Hungarian language accuracy depends on model quality
- GUI is single-threaded (one processing task at a time)

## Future Enhancement Ideas

- [ ] Batch API requests for faster processing
- [ ] Local caching to avoid reprocessing
- [ ] Multi-language support beyond Hungarian
- [ ] Export to database formats
- [ ] Validation rules for output data
- [ ] Undo/redo functionality
- [ ] Search and filter in Excel viewer
- [ ] Progress bar visualization
- [ ] Cost tracking display
- [ ] Support for other LLM providers (Anthropic, etc.)

---

**Package Complete and Ready to Use!**
