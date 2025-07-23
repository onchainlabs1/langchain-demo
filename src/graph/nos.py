from typing import Dict, Any, TypedDict
import pandas as pd
from core.analysis import run_dataframe_analysis


class GraphState(TypedDict):
    """State schema for the LangGraph execution."""
    df: Any  # DataFrame or None
    question: str
    next_node: str
    text_answer: str
    chart_base64: Any  # str or None
    status: str
    message: str


def interpreter(state: GraphState) -> GraphState:
    """
    LangGraph interpreter node.
    Decides whether the user's question should be routed to DataFrame analysis
    or if the flow should be terminated.

    Args:
        state (GraphState): Current state containing the question.

    Returns:
        GraphState: Updated state with next_node decision.
    """
    # Keywords indicating tabular analysis
    keywords = [
        "column", "average", "mean", "graph", "chart", "dataframe", "table",
        "row", "sum", "count", "quantity", "value", "maximum", "minimum"
    ]
    question_lower = state["question"].lower()
    if any(word in question_lower for word in keywords):
        return {**state, "next_node": "run_dataframe_analysis"}
    else:
        return {**state, "next_node": "end"}


def run_dataframe_analysis_node(state: GraphState) -> GraphState:
    """
    LangGraph node responsible for running the DataFrame analysis.
    Receives state with DataFrame and question, calls the analysis function,
    and returns the complete state with answer, chart (if any), status, and message.

    Args:
        state (GraphState): State containing 'df' (DataFrame) and 'question' (str).

    Returns:
        GraphState: Complete state with analysis results.
    """
    try:
        df = state["df"]
        question = state["question"]
        
        # Handle case where DataFrame is None
        if df is None:
            return {
                **state,
                "text_answer": "No data available for analysis. Please upload a file first.",
                "chart_base64": None,
                "status": "ok",
                "message": "No data provided."
            }
        
        answer, chart = run_dataframe_analysis(df, question)
        return {
            **state,
            "text_answer": answer,
            "chart_base64": chart,
            "status": "ok",
            "message": "Analysis completed successfully."
        }
    except Exception as e:
        return {
            **state,
            "text_answer": "",
            "chart_base64": None,
            "status": "error",
            "message": f"Error running analysis: {e}"
        } 