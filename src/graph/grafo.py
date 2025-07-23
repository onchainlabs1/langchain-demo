from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END, START
from graph.nos import interpreter, run_dataframe_analysis_node
import pandas as pd


class GraphState(TypedDict):
    """State schema for the LangGraph execution."""
    df: Any  # DataFrame or None
    question: str
    next_node: str
    text_answer: str
    chart_base64: Any  # str or None
    status: str
    message: str


def end_node(state: GraphState) -> GraphState:
    """
    Node that returns a generic message when the question is not understood or not related to data analysis.
    """
    return {
        **state,
        "text_answer": "Sorry, I cannot answer this type of question at the moment.",
        "chart_base64": None,
        "status": "end",
        "message": "The question was not related to data analysis."
    }


def build_graph():
    """
    Builds and returns the LangGraph execution graph with interpreter, analysis, and end nodes.
    The input is a dictionary with optional 'df' (DataFrame) and 'question' (string).
    """
    # Define the state schema
    graph = StateGraph(GraphState)

    # Register nodes
    graph.add_node("interpreter", interpreter)
    graph.add_node("run_dataframe_analysis_node", run_dataframe_analysis_node)
    graph.add_node("end_node", end_node)

    # For portfolio purposes, we'll use a simplified approach
    # In a real implementation, you would use proper conditional routing
    graph.add_edge(START, "interpreter")
    graph.add_edge("interpreter", "run_dataframe_analysis_node")
    graph.add_edge("run_dataframe_analysis_node", END)
    graph.add_edge("end_node", END)

    return graph.compile() 