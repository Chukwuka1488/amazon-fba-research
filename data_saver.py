# --- Data Saving Logic ---
import os
import pandas as pd
import numpy as np
from typing import List, Dict
from datetime import datetime

# Import configuration and analytics functions
import config
from analytics import (
    sort_by_rank, 
    create_fba_analysis_sheet, 
    create_price_analysis_sheet, 
    create_metadata_sheet
)

def save_to_csv(data: List[Dict[str, str]], filename: str = None) -> None:
    """
    Saves the list of product dictionaries to a CSV file.
    
    Args:
        data: List of product dictionaries to save
        filename: Output filename (optional, uses config if not provided)
    """
    if not filename:
        filename = config.OUTPUT_CSV_FILE
        
    if not data:
        print("No data to save.")
        return
        
    try:
        print(f"Saving {len(data)} products to {filename}...")
        df = pd.DataFrame(data)
        
        # Sort by rank (numerical sorting)
        df = sort_by_rank(df)
        
        # Save without the default pandas index column, ensure UTF-8 encoding
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Data saved successfully to {filename}.")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")
        print("Please check file permissions and disk space.")

def save_to_excel(data: List[Dict[str, str]], filename: str = None) -> None:
    """
    Saves the list of product dictionaries to an Excel file with formatting and analysis.
    
    Args:
        data: List of product dictionaries to save
        filename: Output filename (optional, uses config if not provided)
    """
    if not filename:
        filename = config.OUTPUT_EXCEL_FILE
        
    if not data:
        print("No data to save.")
        return
        
    try:
        print(f"Creating Excel analysis file with {len(data)} products...")
        df = pd.DataFrame(data)
        
        # Sort by rank
        df = sort_by_rank(df)
        
        # Create a timestamp for the report
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Create Excel writer
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='Products', index=False)
            
            # Add analysis sheets
            create_fba_analysis_sheet(df, writer)
            create_price_analysis_sheet(df, writer)
            create_metadata_sheet(df, writer, timestamp)
            
        print(f"Excel analysis file saved successfully to {filename}.")
    except ImportError:
        print("Excel export requires openpyxl. Installing...")
        try:
            import subprocess
            subprocess.check_call(["pip", "install", "openpyxl"])
            print("openpyxl installed, retrying export...")
            save_to_excel(data, filename)
        except Exception as e:
            print(f"Failed to install openpyxl: {e}")
            print("Falling back to CSV export")
            save_to_csv(data)
    except Exception as e:
        print(f"Error saving data to Excel: {e}")
        print("Falling back to CSV export...")
        save_to_csv(data)

def save_all_formats(data: List[Dict[str, str]]) -> None:
    """Save data to both CSV and Excel formats"""
    save_to_csv(data)
    save_to_excel(data)