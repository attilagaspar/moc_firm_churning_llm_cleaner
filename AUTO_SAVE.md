# Auto-Save Feature

## Overview

The application now automatically saves your progress after each row is processed. This means:

- **No more manual saves required** - The app saves continuously as it works
- **Resume from where you left off** - If the app crashes or you stop it, you can resume exactly where you left off
- **Fixed output filenames** - Output files are named consistently based on the input file

## How It Works

### 1. Fixed Output Filename

When you open an input file like `1899_tables_raw_bycolumn_8columns.xlsx`, the app creates a fixed output file:
```
output/1899_tables_raw_bycolumn_8columns_cleaned.xlsx
```

This file is updated after each row is processed.

### 2. Automatic Resume

When you open the same input file again:
- The app checks if `output/[filename]_cleaned.xlsx` exists
- If it does, it loads the progress file instead of the original
- It automatically selects the first unprocessed row
- You can click **Play** to continue processing from there

### 3. Progress Tracking

The app tracks progress by checking the `cleaning_date` column:
- Empty = not processed yet
- Has a date = already processed

### 4. Manual Saves (Optional)

You can still use **File > Save Excel** to create timestamped backups:
```
output/1899_tables_raw_bycolumn_8columns_cleaned_20260205_143022.xlsx
```

These timestamped files are useful for:
- Creating milestone backups
- Comparing different processing runs
- Archiving completed work

## Example Workflow

1. **Open your data file**: `File > Open Excel` → select `1899_tables_raw.xlsx`
2. **Start processing**: Select row 0 → click **▶ Play**
3. **App saves automatically** after each row
4. **If you need to stop**: Click **⏹ Stop** (current progress is saved)
5. **Close the application**
6. **Resume later**: `File > Open Excel` → select same file
   - App loads your progress automatically
   - Shows message: "Loaded progress: 50/100 rows done. Select row 50 to resume."
   - Row 50 is automatically selected
   - Click **▶ Play** to continue

## Benefits

- **Safe from crashes**: Power outage? No problem - restart and resume
- **Interruptible**: Stop and resume anytime without losing work
- **Transparent**: Always see your progress in the status bar
- **No manual save needed**: Just process and go
- **Consistent naming**: Easy to find your output files

## Technical Details

### File Format
- Auto-save format: `.xlsx` (Excel)
- Uses the same format as the input file
- Preserves all columns from the original data

### Save Trigger
The app saves after:
- Each single row lookup (🔍 Lookup button)
- Each row during auto-processing (▶ Play button)

### Progress Detection
A row is considered "processed" if:
- The `cleaning_date` column has a value
- This timestamp indicates when the LLM processed that row

### Output Location
All auto-save files are stored in the `output/` directory at the root of the project.
