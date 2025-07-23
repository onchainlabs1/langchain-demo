from typing import Dict, Any
import pandas as pd
from core.analysis import run_dataframe_analysis


def interpreter(question: str) -> Dict[str, str]:
    """
    LangGraph interpreter node.
    Decides whether the user's question should be routed to DataFrame analysis
    or if the flow should be terminated.

    Args:
        question (str): User's question in Portuguese.

    Returns:
        dict: Dictionary with the key 'next_node', indicating the next node in the flow.
              Can be 'run_dataframe_analysis' or 'end'.
    """
    # Keywords indicating tabular analysis
    keywords = [
        "column", "average", "mean", "graph", "chart", "dataframe", "table",
        "row", "sum", "count", "quantity", "value", "maximum", "minimum"
    ]
    question_lower = question.lower()
    if any(word in question_lower for word in keywords):
        return {"next_node": "run_dataframe_analysis"}
    else:
        return {"next_node": "end"}


def run_dataframe_analysis_node(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph node responsible for running the DataFrame analysis.
    Receives a dictionary with the DataFrame and the question, calls the analysis function,
    and returns the answer, chart (if any), status, and a message for logs.

    Args:
        input_data (dict): Must contain the keys 'df' (DataFrame) and 'question' (str).

    Returns:
        dict: Contains 'text_answer', 'chart_base64', 'status', and 'message'.
    """
    try:
        df = input_data["df"]
        question = input_data["question"]
        answer, chart = run_dataframe_analysis(df, question)
        return {
            "text_answer": answer,
            "chart_base64": chart,
            "status": "ok",
            "message": "Analysis completed successfully."
        }
    except Exception as e:
        return {
            "text_answer": "",
            "chart_base64": None,
            "status": "error",
            "message": f"Error running analysis: {e}"
        } 