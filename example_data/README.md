# Example Data Directory

## Current Files

- `1899_tables_raw_bycolumn_8columns.xlsx` - Your input data file

## Expected Excel Format

Your Excel file should have **9 columns** in this order:

1. **Court** - Court registration location (e.g., "Budapesti Királyi Törvényszék")
2. **Date and Legal ID** - Combined field (e.g., "1898. jun. 15. 1234/98")
3. **Firm Name** - Name of the company (e.g., "Szabó és Társa")
4. **Firm Location** - Main location (e.g., "Pozsony", "Budapest")
5. **Owner** - Owner name(s) (Czég birtokosa)
6. **Managers** - Manager name(s) (Czégvezetők)
7. **[Ignored]** - Badly scanned vertical column (will be ignored)
8. **Notes** - Event details in Hungarian (**most important column**)
9. **Source** - Source filename or identifier

## Notes About the Data

### Court Field
- May contain the "macskaköröm" symbol (") meaning "same as above"
- The LLM will interpret this correctly

### Date and Legal ID Field
- Usually in format: "YEAR. MONTH. DAY. LEGAL_ID"
- Example: "1898. június 15. 1234/98"
- The LLM will separate the date and legal identifier

### Firm Name
- May have OCR errors like spacing: "S z a b ó  és  T á r s a"
- The LLM will clean these to: "Szabó és Társa"

### Location
- May have OCR spacing errors: "P o z s o n y" → "Pozsony"
- Historical Hungarian place names (Pozsony = Bratislava)

### Owner and Managers
- May be semicolon or comma-separated
- May have OCR errors
- LLM will clean and standardize

### Notes Column (Critical!)
This column contains the actual event information:
- What type of event occurred
- Who entered or left the firm
- Changes in legal status
- References to other gazette entries
- Details about the business change

Examples:
- "A czég törlése a czégjegyzékből..." (Firm deletion)
- "Új tagok belépése..." (New members joining)
- "Czégforma változás..." (Legal form change)

### Source
- Filename or identifier of the scanned page
- Useful for tracking back to original documents

## File Formats Supported

- `.xlsx` (Excel 2007+) - Recommended
- `.xls` (Excel 97-2003) - Also supported

## Adding New Files

1. Place your Excel files in this directory
2. Ensure they follow the 9-column format above
3. Use File → Open in the application to load them

## Tips

- Keep original files as backups
- The application does not modify input files
- Processed files are saved to `output/` directory
- Files can have any name - format matters, not filename

## Validation

Before processing, verify:
- ✅ File has 9 columns (8th column may be mostly empty - that's OK)
- ✅ Column 8 (Notes) has substantial Hungarian text
- ✅ Rows represent individual firm events
- ✅ File opens correctly in Excel

---

Your current file `1899_tables_raw_bycolumn_8columns.xlsx` appears to be correctly formatted!
