# Prompt Templates for Hungarian Firm Registry Cleaner

This directory contains prompt templates and documentation for the LLM data cleaning process.

## Current Prompt Structure

The main prompt is defined in `src/config.py` and consists of:

1. **System Prompt**: Establishes the AI's role as an expert in Hungarian historical documents
2. **User Prompt**: Provides the specific data row and instructions for structured output

## Customizing Prompts

To modify the prompts:

1. Edit `src/config.py`
2. Modify `SYSTEM_PROMPT` for the AI's general behavior
3. Modify `USER_PROMPT_TEMPLATE` for specific instructions
4. Restart the application to apply changes

## Example Customizations

### Adding Context About Specific Regions

Add to SYSTEM_PROMPT:
```python
Additional context: 
- Pozsony is the Hungarian name for Bratislava
- Fiume is Rijeka in modern-day Croatia
- Common Hungarian legal forms: kft. (limited liability), rt. (joint-stock), bt. (partnership)
```

### Adjusting Output Requirements

Modify USER_PROMPT_TEMPLATE to add or remove fields:
```python
"additional_info": "Any additional relevant information from the notes",
```

### Changing Classification Scheme

Update EVENT_TYPES in config.py:
```python
EVENT_TYPES = {
    1: "Firm birth",
    2: "Firm death",
    3: "Ownership change",
    4: "Management change",
    5: "Legal status change",
    6: "Address change",
    7: "Capital change",
    8: "Other"
}
```

## Best Practices

1. **Be Specific**: Provide clear examples in the prompt
2. **Use Structured Output**: The JSON schema ensures consistent responses
3. **Low Temperature**: Set to 0.1 for consistency (defined in llm_processor.py)
4. **Test Changes**: Always test on sample data before batch processing

## Hungarian Language Notes

Important Hungarian terms the AI should recognize:

- **Czég** = Firm/Company (older spelling)
- **Cég** = Firm/Company (modern spelling)
- **Birtokosa** = Owner/Possessor
- **Vezetők** = Managers/Directors
- **Bejegyzés** = Registration
- **Törlés** = Deletion/Dissolution
- **Változás** = Change
- **Kft.** = Korlátolt Felelősségű Társaság (Ltd.)
- **Rt.** = Részvénytársaság (Joint-stock company)
- **Bt.** = Betéti Társaság (Partnership)

## Common OCR Issues

The AI is trained to fix:

1. **Spacing errors**: "P o z s o n y" → "Pozsony"
2. **Character confusion**: "l" vs "I", "0" vs "O"
3. **Hungarian diacritics**: Missing or wrong accents (á, é, í, ó, ö, ő, ú, ü, ű)
4. **Date format**: Various formats → "YYYY.MM.DD."
5. **Layout artifacts**: Text split across lines or columns

## Future Enhancements

Consider adding:
- Few-shot examples in the prompt
- Entity type definitions (person names vs. place names)
- Industry classification
- Historical context validation
