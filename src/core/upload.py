"""
File upload and validation module for the Data Analyst Agent.
"""

import pandas as pd
import io
from typing import Union, Any
from pathlib import Path


def validate_file_upload(uploaded_file: Union[str, io.StringIO, Any]) -> pd.DataFrame:
    """
    Validate and load an uploaded file into a pandas DataFrame.
    
    Args:
        uploaded_file: File object or path to validate and load
        
    Returns:
        pd.DataFrame: Loaded and validated DataFrame
        
    Raises:
        ValueError: If file format is not supported or validation fails
        Exception: If file cannot be loaded
    """
    try:
        # Handle different file types
        if hasattr(uploaded_file, 'name'):
            file_name = uploaded_file.name.lower()
        elif isinstance(uploaded_file, str):
            file_name = uploaded_file.lower()
        else:
            file_name = "unknown"
        
        # Load based on file extension
        if file_name.endswith('.csv'):
            if isinstance(uploaded_file, str):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
        elif file_name.endswith(('.xlsx', '.xls')):
            if isinstance(uploaded_file, str):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        elif file_name.endswith('.json'):
            if isinstance(uploaded_file, str):
                df = pd.read_json(uploaded_file)
            else:
                df = pd.read_json(uploaded_file)
        elif file_name.endswith('.parquet'):
            if isinstance(uploaded_file, str):
                df = pd.read_parquet(uploaded_file)
            else:
                df = pd.read_parquet(uploaded_file)
        else:
            raise ValueError("Unsupported file format. Please upload CSV, Excel, JSON, or Parquet files.")
        
        # Basic validation
        if df.empty:
            raise ValueError("The uploaded file contains no data.")
        
        if len(df.columns) == 0:
            raise ValueError("The uploaded file has no columns.")
        
        # Limit file size (approximate)
        if len(df) > 10000:
            raise ValueError("File too large. Please upload files with fewer than 10,000 rows.")
        
        return df
        
    except Exception as e:
        if "Unsupported file format" in str(e):
            raise e
        elif "contains no data" in str(e):
            raise e
        elif "has no columns" in str(e):
            raise e
        elif "too large" in str(e):
            raise e
        else:
            raise ValueError(f"Error loading file: {str(e)}")


def get_file_info(df: pd.DataFrame) -> dict:
    """
    Get basic information about the loaded DataFrame.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        dict: Information about the DataFrame
    """
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": dict(df.dtypes),
        "missing_values": df.isnull().sum().to_dict(),
        "memory_usage": df.memory_usage(deep=True).sum()
    } 