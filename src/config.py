"""
Configuration file for LLM Data Cleaner
Contains prompts, model settings, and column mappings
"""

from datetime import datetime

# OpenAI Model Options
AVAILABLE_MODELS = [
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-3.5-turbo"
]

DEFAULT_MODEL = "gpt-4o-mini"

# Input Column Names (Expected order in Excel)
INPUT_COLUMNS = {
    0: "court",
    1: "date_and_legal_id",
    2: "firm_name",
    3: "firm_location",
    4: "owner",
    5: "managers",
    6: "ignored_column",
    7: "notes",
    8: "source"
}

# Output Column Names
OUTPUT_COLUMNS = [
    "cleaned_court",
    "cleaned_date",
    "legal_identifier",
    "cleaned_firm_name",
    "cleaned_location",
    "cleaned_owners",
    "cleaned_managers",
    "cleaned_notes_hu",
    "notes_english",
    "event_classification",
    "names_incoming",
    "names_outgoing",
    "gazette_references",
    "model_used",
    "cleaning_date"
]

# Event Classification Types
EVENT_TYPES = {
    1: "Firm birth (registration)",
    2: "Firm death (dissolution)",
    3: "Ownership change",
    4: "Management change",
    5: "Change in legal status",
    6: "Other"
}

# System Prompt for LLM
SYSTEM_PROMPT = """You are an expert in Hungarian historical documents, specifically the "Központi Értesítő" (Central Gazette) from turn of the 19th-20th century Hungary. Your task is to clean OCR errors from scanned firm registry documents and extract structured information.

Key responsibilities:
1. Fix OCR errors (spelling mistakes, layout issues like "P o z s o n y" → "Pozsony")
2. Handle "macskaköröm" (") which means "same as above entry"
3. Extract and structure firm information
4. Recognize Hungarian entity names (locations, firms, people)
5. Classify registry events
6. Translate Hungarian notes to English

Be precise and maintain historical accuracy. If information is unclear or missing, indicate this in your response."""

# User Prompt Template
USER_PROMPT_TEMPLATE = """Please process the following Hungarian firm registry entry and return a JSON object with cleaned and structured data.

Input data:
- Court: {court}
- Date and Legal ID: {date_and_legal_id}
- Firm Name: {firm_name}
- Firm Location: {firm_location}
- Owner: {owner}
- Managers: {managers}
- Notes (Hungarian): {notes}
- Source: {source}

Please return a JSON object with the following fields:
{{
    "cleaned_court": "Cleaned court name (if " symbol, indicate 'same as above')",
    "cleaned_date": "Date in YYYY.MM.DD. format",
    "legal_identifier": "Legal identifier extracted from date field",
    "cleaned_firm_name": "Cleaned firm name with OCR errors fixed",
    "cleaned_location": "Cleaned location name",
    "cleaned_owners": "Cleaned owner name(s), semicolon-separated if multiple",
    "cleaned_managers": "Cleaned manager name(s), semicolon-separated if multiple",
    "cleaned_notes_hu": "Cleaned Hungarian text of notes with OCR errors fixed",
    "notes_english": "English summary/translation of the notes",
    "event_classification": 1-6 (1=firm birth, 2=firm death, 3=ownership change, 4=management change, 5=legal status change, 6=other),
    "names_incoming": "Names entering ownership/management (from notes), semicolon-separated",
    "names_outgoing": "Names leaving ownership/management (from notes), semicolon-separated",
    "gazette_references": "Any references to other Central Gazette issues from notes"
}}

Important notes:
- Fix spacing issues in names (e.g., "P o z s o n y" → "Pozsony")
- Preserve Hungarian characters (á, é, í, ó, ö, ő, ú, ü, ű)
- Be precise with dates - follow Hungarian date format
- For event classification, choose the most appropriate category
- If multiple people are involved, separate with semicolons
- Return ONLY valid JSON, no additional text"""

# Alternative structured output format using OpenAI's structured outputs
RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "firm_registry_entry",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "cleaned_court": {"type": "string"},
                "cleaned_date": {"type": "string"},
                "legal_identifier": {"type": "string"},
                "cleaned_firm_name": {"type": "string"},
                "cleaned_location": {"type": "string"},
                "cleaned_owners": {"type": "string"},
                "cleaned_managers": {"type": "string"},
                "cleaned_notes_hu": {"type": "string"},
                "notes_english": {"type": "string"},
                "event_classification": {"type": "integer", "minimum": 1, "maximum": 6},
                "names_incoming": {"type": "string"},
                "names_outgoing": {"type": "string"},
                "gazette_references": {"type": "string"}
            },
            "required": [
                "cleaned_court",
                "cleaned_date",
                "legal_identifier",
                "cleaned_firm_name",
                "cleaned_location",
                "cleaned_owners",
                "cleaned_managers",
                "cleaned_notes_hu",
                "notes_english",
                "event_classification",
                "names_incoming",
                "names_outgoing",
                "gazette_references"
            ],
            "additionalProperties": False
        }
    }
}

def get_current_timestamp():
    """Return current timestamp in ISO format"""
    return datetime.now().isoformat()
