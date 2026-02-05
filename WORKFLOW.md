# Application Workflow Diagram

## Data Flow

```
┌─────────────────┐
│  Excel File     │
│  (.xls/.xlsx)   │
│  example_data/  │
└────────┬────────┘
         │
         │ Load
         ▼
┌─────────────────────────────┐
│   DataHandler               │
│   - Loads Excel             │
│   - Manages DataFrame       │
│   - Adds output columns     │
└────────┬────────────────────┘
         │
         │ Row Selection
         ▼
┌─────────────────────────────┐
│   GUI (main.py)             │
│   ┌─────────────────────┐   │
│   │ Excel Viewer        │   │
│   │ (Treeview)          │   │
│   └─────────────────────┘   │
│                             │
│   [Model: gpt-4o-mini ▼]    │
│   [🔍 Lookup] [▶ Play]      │
│   [⏹ Stop]                  │
└────────┬────────────────────┘
         │
         │ Selected Row Data
         ▼
┌─────────────────────────────┐
│   LLMProcessor              │
│   - Formats prompt          │
│   - Calls OpenAI API        │
│   - Parses JSON response    │
└────────┬────────────────────┘
         │
         │ Structured JSON
         ▼
┌─────────────────────────────┐
│   Cleaned Data              │
│   {                         │
│     "cleaned_court": "...", │
│     "cleaned_date": "...",  │
│     "event_classification": │
│     ...                     │
│   }                         │
└────────┬────────────────────┘
         │
         ├──────────┬──────────┐
         │          │          │
         ▼          ▼          ▼
    ┌────────┐ ┌───────┐ ┌─────────┐
    │DataFrame│ │ GUI   │ │ Output  │
    │Updated  │ │Display│ │ Files   │
    └────────┘ └───────┘ └─────────┘
         │          │          │
         │          │          ├─> .xlsx
         │          │          └─> .json
         │          │
         └──────────┴──> Continue to next row
```

## User Interaction Flow

```
START
  │
  ├─> Open Application (main.py)
  │
  ├─> 📂 Open Excel File
  │     │
  │     └─> Browse to example_data/
  │           │
  │           └─> File loads into GUI
  │
  ├─> Select Model (dropdown)
  │     │
  │     └─> gpt-4o-mini | gpt-4o | gpt-4-turbo | gpt-3.5-turbo
  │
  ├─> OPTION A: Single Row Processing
  │     │
  │     ├─> Click on row in table
  │     ├─> Click "🔍 Lookup"
  │     ├─> Wait 5-15 seconds
  │     ├─> View JSON output
  │     └─> Repeat for next row
  │
  └─> OPTION B: Batch Processing
        │
        ├─> Click on starting row
        ├─> Click "▶ Play"
        ├─> Confirm dialog
        ├─> Watch progress
        │     │
        │     ├─> See current row highlighted
        │     ├─> See JSON output updating
        │     ├─> See status bar progress
        │     │
        │     └─> Optional: Click "⏹ Stop" to pause
        │
        └─> Processing complete
              │
              ├─> File → Save Excel
              ├─> File → Save JSON
              └─> Check output/ folder
```

## Component Architecture

```
┌─────────────────────────────────────────────────┐
│                    main.py                      │
│         (FirmRegistryCleanerGUI)                │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │  GUI Layer (tkinter)                     │  │
│  │  - Treeview (Excel display)              │  │
│  │  - ScrolledText (JSON output)            │  │
│  │  - Buttons, Dropdowns, Status            │  │
│  └──────────────────────────────────────────┘  │
│                     │                           │
│                     │ Uses                      │
│                     ▼                           │
│  ┌──────────────────────────────────────────┐  │
│  │  Business Logic                          │  │
│  │  - Row selection handling                │  │
│  │  - Threading management                  │  │
│  │  - Auto-processing loop                  │  │
│  │  - Error handling                        │  │
│  └──────────────────────────────────────────┘  │
└───────────────┬─────────────────┬───────────────┘
                │                 │
                │ Uses            │ Uses
                ▼                 ▼
    ┌───────────────────┐  ┌──────────────────┐
    │  data_handler.py  │  │ llm_processor.py │
    │  (DataHandler)    │  │ (LLMProcessor)   │
    │                   │  │                  │
    │  - load_excel()   │  │ - process_row()  │
    │  - save_excel()   │  │ - _call_openai() │
    │  - save_json()    │  │ - _parse_resp()  │
    │  - update_row()   │  │                  │
    └─────────┬─────────┘  └────────┬─────────┘
              │                     │
              │ Uses                │ Uses
              ▼                     ▼
    ┌───────────────────────────────────────┐
    │           config.py                   │
    │                                       │
    │  - AVAILABLE_MODELS                   │
    │  - INPUT_COLUMNS / OUTPUT_COLUMNS     │
    │  - SYSTEM_PROMPT                      │
    │  - USER_PROMPT_TEMPLATE               │
    │  - RESPONSE_FORMAT (JSON schema)      │
    │  - EVENT_TYPES                        │
    └───────────────────────────────────────┘
```

## Threading Model

```
Main Thread (GUI)
  │
  ├─> GUI Event Loop
  │   - Button clicks
  │   - Dropdown changes
  │   - Row selections
  │
  └─> Spawns Worker Threads
        │
        ├─> Single Row Processing Thread
        │   └─> _process_single_row()
        │
        └─> Auto-Processing Thread
            └─> _auto_process_rows()
                  │
                  └─> Loop through rows
                        ├─> Call LLM API
                        ├─> Update DataFrame
                        ├─> Update GUI (via .after())
                        └─> Check stop_requested flag
```

## Data Transformation Example

```
INPUT (Excel Row):
┌────────────────────────────────────────────────────┐
│ Court: "                                           │
│ Date: "1898. jun. 15. 1234/98                     │
│ Name: "S z a b ó  és  Társa                       │
│ Location: "P o z s o n y                           │
│ Owner: "Szabó János                                │
│ Managers: "Kiss Péter, Nagy László                 │
│ Notes: "A czég törlése a czégjegyzékből...         │
└────────────────────────────────────────────────────┘
                      │
                      │ LLM Processing
                      ▼
OUTPUT (JSON):
┌────────────────────────────────────────────────────┐
│ {                                                  │
│   "cleaned_court": "same as above",                │
│   "cleaned_date": "1898.06.15.",                   │
│   "legal_identifier": "1234/98",                   │
│   "cleaned_firm_name": "Szabó és Társa",           │
│   "cleaned_location": "Pozsony",                   │
│   "cleaned_owners": "Szabó János",                 │
│   "cleaned_managers": "Kiss Péter; Nagy László",   │
│   "cleaned_notes_hu": "A cég törlése...",          │
│   "notes_english": "Deletion of firm from...",     │
│   "event_classification": 2,                       │
│   "names_incoming": "",                            │
│   "names_outgoing": "Szabó János",                 │
│   "gazette_references": "",                        │
│   "model_used": "gpt-4o-mini",                     │
│   "cleaning_date": "2026-02-04T15:30:00"           │
│ }                                                  │
└────────────────────────────────────────────────────┘
```

## File Operations

```
INPUT:
  example_data/
    └─ firms_1898.xlsx  (Original file, preserved)

PROCESSING:
  (In-memory DataFrame with added columns)

OUTPUT:
  output/
    ├─ firms_1898_cleaned_20260204_153000.xlsx
    └─ firms_1898_cleaned_20260204_153000.json
```

## Error Handling Flow

```
Try Process Row
  │
  ├─> Success
  │   ├─> Update DataFrame
  │   ├─> Update GUI
  │   └─> Continue
  │
  └─> Error
      ├─> Catch Exception
      ├─> Display error in JSON output
      ├─> Show dialog to user
      ├─> Log error with row number
      └─> Ask: Continue or Stop?
            │
            ├─> Continue → Next row
            └─> Stop → End processing
```

---

This diagram explains the complete workflow from data input to processed output, 
showing how all components interact with each other.
