"""
LLM Processor Module
Handles OpenAI API interactions for cleaning firm registry data
"""

import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from src.config import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    RESPONSE_FORMAT,
    INPUT_COLUMNS,
    get_current_timestamp
)

# Load environment variables
load_dotenv()


class LLMProcessor:
    """Handles LLM API calls for data cleaning"""
    
    def __init__(self, model="gpt-4o-mini"):
        """
        Initialize the LLM processor
        
        Args:
            model: OpenAI model to use (default: gpt-4o-mini)
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY in .env file"
            )
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def process_row(self, row_data):
        """
        Process a single row of firm registry data
        
        Args:
            row_data: Dictionary or pandas Series with row data
            
        Returns:
            dict: Cleaned and structured data with metadata
        """
        # Extract input fields
        input_fields = self._extract_input_fields(row_data)
        
        # Create prompt
        user_prompt = self._create_prompt(input_fields)
        
        # Call OpenAI API
        try:
            response = self._call_openai_api(user_prompt)
            
            # Parse response
            cleaned_data = self._parse_response(response)
            
            # Add metadata
            cleaned_data["model_used"] = self.model
            cleaned_data["cleaning_date"] = get_current_timestamp()
            
            return cleaned_data
            
        except Exception as e:
            # Return error information
            return {
                "error": str(e),
                "model_used": self.model,
                "cleaning_date": get_current_timestamp()
            }
    
    def _extract_input_fields(self, row_data):
        """Extract input fields from row data"""
        # Handle both dictionary and pandas Series
        if hasattr(row_data, 'iloc'):
            # Pandas Series - access by position
            return {
                'court': str(row_data.iloc[0]) if len(row_data) > 0 else "",
                'date_and_legal_id': str(row_data.iloc[1]) if len(row_data) > 1 else "",
                'firm_name': str(row_data.iloc[2]) if len(row_data) > 2 else "",
                'firm_location': str(row_data.iloc[3]) if len(row_data) > 3 else "",
                'owner': str(row_data.iloc[4]) if len(row_data) > 4 else "",
                'managers': str(row_data.iloc[5]) if len(row_data) > 5 else "",
                'notes': str(row_data.iloc[7]) if len(row_data) > 7 else "",
                'source': str(row_data.iloc[8]) if len(row_data) > 8 else ""
            }
        else:
            # Dictionary - access by key
            return {
                'court': str(row_data.get('court', '')),
                'date_and_legal_id': str(row_data.get('date_and_legal_id', '')),
                'firm_name': str(row_data.get('firm_name', '')),
                'firm_location': str(row_data.get('firm_location', '')),
                'owner': str(row_data.get('owner', '')),
                'managers': str(row_data.get('managers', '')),
                'notes': str(row_data.get('notes', '')),
                'source': str(row_data.get('source', ''))
            }
    
    def _create_prompt(self, input_fields):
        """Create the user prompt from input fields"""
        return USER_PROMPT_TEMPLATE.format(**input_fields)
    
    def _call_openai_api(self, user_prompt):
        """
        Call OpenAI API with structured output
        
        Args:
            user_prompt: The formatted prompt
            
        Returns:
            str: JSON response from API
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format=RESPONSE_FORMAT,
            temperature=0.1  # Low temperature for consistency
        )
        
        return response.choices[0].message.content
    
    def _parse_response(self, response):
        """
        Parse JSON response from API
        
        Args:
            response: JSON string response
            
        Returns:
            dict: Parsed data
        """
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse LLM response as JSON: {e}")
    
    def set_model(self, model):
        """Change the model being used"""
        self.model = model
