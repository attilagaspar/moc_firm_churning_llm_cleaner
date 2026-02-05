"""
Data Handler Module
Handles Excel and JSON file operations
"""

import pandas as pd
import json
import os
from datetime import datetime
from src.config import OUTPUT_COLUMNS


class DataHandler:
    """Handles loading, saving, and managing data"""
    
    def __init__(self):
        """Initialize the data handler"""
        self.df = None
        self.file_path = None
        self.output_dir = "output"
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def load_excel(self, file_path):
        """
        Load Excel file
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            pandas.DataFrame: Loaded data
        """
        try:
            # Try to read as xlsx first, then xls
            if file_path.endswith('.xlsx'):
                self.df = pd.read_excel(file_path, engine='openpyxl')
            elif file_path.endswith('.xls'):
                self.df = pd.read_excel(file_path, engine='xlrd')
            else:
                # Try both engines
                try:
                    self.df = pd.read_excel(file_path, engine='openpyxl')
                except:
                    self.df = pd.read_excel(file_path, engine='xlrd')
            
            self.file_path = file_path
            
            # Initialize output columns if they don't exist
            self._initialize_output_columns()
            
            return self.df
            
        except Exception as e:
            raise Exception(f"Failed to load Excel file: {e}")
    
    def _initialize_output_columns(self):
        """Add output columns to dataframe if they don't exist"""
        for col in OUTPUT_COLUMNS:
            if col not in self.df.columns:
                self.df[col] = ""
    
    def get_row(self, index):
        """
        Get a specific row
        
        Args:
            index: Row index
            
        Returns:
            pandas.Series: Row data
        """
        if self.df is None:
            raise ValueError("No data loaded")
        
        if index < 0 or index >= len(self.df):
            raise IndexError(f"Row index {index} out of range")
        
        return self.df.iloc[index]
    
    def update_row(self, index, cleaned_data):
        """
        Update a row with cleaned data
        
        Args:
            index: Row index
            cleaned_data: Dictionary with cleaned data
        """
        if self.df is None:
            raise ValueError("No data loaded")
        
        # Update each output column
        for col in OUTPUT_COLUMNS:
            if col in cleaned_data:
                self.df.at[index, col] = cleaned_data[col]
    
    def save_excel(self, output_path=None):
        """
        Save DataFrame to Excel
        
        Args:
            output_path: Output file path (optional)
            
        Returns:
            str: Path where file was saved
        """
        if self.df is None:
            raise ValueError("No data to save")
        
        if output_path is None:
            # Generate output path based on input file
            base_name = os.path.basename(self.file_path)
            name, ext = os.path.splitext(base_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(
                self.output_dir,
                f"{name}_cleaned_{timestamp}.xlsx"
            )
        
        # Save to Excel
        self.df.to_excel(output_path, index=False, engine='openpyxl')
        
        return output_path
    
    def save_json(self, output_path=None):
        """
        Save DataFrame to JSON
        
        Args:
            output_path: Output file path (optional)
            
        Returns:
            str: Path where file was saved
        """
        if self.df is None:
            raise ValueError("No data to save")
        
        if output_path is None:
            # Generate output path based on input file
            base_name = os.path.basename(self.file_path)
            name, ext = os.path.splitext(base_name)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(
                self.output_dir,
                f"{name}_cleaned_{timestamp}.json"
            )
        
        # Convert to JSON (orient='records' gives list of dicts)
        json_data = self.df.to_dict(orient='records')
        
        # Save to file with proper formatting
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        return output_path
    
    def get_dataframe(self):
        """Return the current dataframe"""
        return self.df
    
    def get_row_count(self):
        """Return number of rows"""
        if self.df is None:
            return 0
        return len(self.df)
    
    def export_row_json(self, index):
        """
        Export a single row as JSON string
        
        Args:
            index: Row index
            
        Returns:
            str: JSON formatted string
        """
        if self.df is None:
            raise ValueError("No data loaded")
        
        row = self.df.iloc[index].to_dict()
        return json.dumps(row, ensure_ascii=False, indent=2)
