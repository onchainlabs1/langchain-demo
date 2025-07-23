import base64
import io
import ast
from typing import Tuple, Optional
import pandas as pd

from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_sandbox import PyodideSandbox
from langgraph.graph import StateGraph, END

# For now, we'll use a mock LLM to avoid external dependencies
# Replace with your preferred LLM and secure configuration
# from langchain_openai import ChatOpenAI

def run_dataframe_analysis(
    df: pd.DataFrame, 
    question: str
) -> Tuple[str, Optional[str]]:
    """
    Securely runs an analysis on a DataFrame based on a natural language question,
    using LangChain, LangGraph, and Pyodide sandbox for Python code execution.

    Args:
        df (pd.DataFrame): DataFrame with the data to be analyzed.
        question (str): User's question in English.

    Returns:
        Tuple[str, Optional[str]]: 
            - Textual answer in English.
            - Chart image in base64 (if generated), or None.
    """
    # For portfolio purposes, we'll use a simplified approach
    # In a real implementation, you would use an actual LLM here
    
    # Simple keyword-based analysis for demonstration
    question_lower = question.lower()
    
    # Get available numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    
    if "average" in question_lower or "mean" in question_lower:
        # Try to find a column mentioned in the question
        for col in numeric_columns:
            if col.lower() in question_lower:
                avg_value = df[col].mean()
                return f"The average {col} is {avg_value:.2f}", None
        
        # If no specific column found, show averages for all numeric columns
        if numeric_columns:
            result = "Averages for numeric columns:\n"
            for col in numeric_columns:
                avg_value = df[col].mean()
                result += f"- {col}: {avg_value:.2f}\n"
            return result, None
    
    elif "sum" in question_lower:
        # Try to find a column mentioned in the question
        for col in numeric_columns:
            if col.lower() in question_lower:
                total_value = df[col].sum()
                return f"The total {col} is {total_value:.2f}", None
        
        # If no specific column found, show sums for all numeric columns
        if numeric_columns:
            result = "Sums for numeric columns:\n"
            for col in numeric_columns:
                total_value = df[col].sum()
                result += f"- {col}: {total_value:.2f}\n"
            return result, None
    
    elif "count" in question_lower:
        count = len(df)
        return f"There are {count} records in the dataset", None
    
    elif "trend" in question_lower or "summary" in question_lower:
        # Provide a general summary
        result = f"Dataset Summary:\n"
        result += f"- Total records: {len(df)}\n"
        result += f"- Columns: {', '.join(df.columns)}\n"
        if numeric_columns:
            result += f"- Numeric columns: {', '.join(numeric_columns)}\n"
        return result, None
    
    else:
        return "I can help you analyze this data. Try asking about averages, sums, counts, or trends of specific columns.", None 