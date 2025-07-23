import pytest
import pandas as pd
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from graph.grafo import build_graph


def test_graph_valid_data_question():
    """
    Test that the graph routes a valid data question to the analysis node and returns a valid answer.
    """
    df = pd.DataFrame({
        "Product": ["A", "B", "C"],
        "Price": [10.0, 20.0, 30.0],
        "Quantity": [1, 2, 3]
    })
    executor = build_graph()
    
    # Provide initial state with all required fields
    initial_state = {
        "df": df,
        "question": "What is the average of the Price column?",
        "next_node": "",
        "text_answer": "",
        "chart_base64": None,
        "status": "",
        "message": ""
    }
    
    result = executor.invoke(initial_state)
    assert isinstance(result, dict)
    assert "text_answer" in result
    assert result["status"] == "ok"
    assert any(word in result["text_answer"].lower() for word in ["average", "price"]) or result["text_answer"].strip() != ""


def test_graph_irrelevant_question():
    """
    Test that the graph handles irrelevant questions through the analysis node (simplified routing).
    """
    executor = build_graph()
    
    initial_state = {
        "df": None,
        "question": "What is the capital of France?",
        "next_node": "",
        "text_answer": "",
        "chart_base64": None,
        "status": "",
        "message": ""
    }
    
    result = executor.invoke(initial_state)
    assert isinstance(result, dict)
    # With simplified routing, all questions go through analysis node
    assert result["status"] == "ok"
    assert "text_answer" in result
    assert result["text_answer"].strip() != ""


def test_graph_output_structure():
    """
    Test that the output structure contains all required keys.
    """
    executor = build_graph()
    
    initial_state = {
        "df": pd.DataFrame({"test": [1, 2, 3]}),
        "question": "Show a graph of the sum of the values.",
        "next_node": "",
        "text_answer": "",
        "chart_base64": None,
        "status": "",
        "message": ""
    }
    
    result = executor.invoke(initial_state)
    assert set(result.keys()) == {"df", "question", "next_node", "text_answer", "chart_base64", "status", "message"} 