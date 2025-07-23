import pytest
import pandas as pd
import re
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from graph.nos import interpreter, run_dataframe_analysis_node


def test_interpreter_tabular_analysis():
    question = "What is the average of column A?"
    state = {"question": question, "next_node": ""}
    result = interpreter(state)
    assert result["next_node"] == "run_dataframe_analysis", "Should route to DataFrame analysis."


def test_interpreter_general_question():
    question = "What is the capital of France?"
    state = {"question": question, "next_node": ""}
    result = interpreter(state)
    assert result["next_node"] == "end", "Should end for non-tabular questions."


def test_interpreter_keyword_variation():
    question = "Show a graph of the sum of the values."
    state = {"question": question, "next_node": ""}
    result = interpreter(state)
    assert result["next_node"] == "run_dataframe_analysis", "Should route to DataFrame analysis."


def test_interpreter_case_insensitive():
    question = "WhAt Is ThE AvErAgE Of CoLuMn price?"
    state = {"question": question, "next_node": ""}
    result = interpreter(state)
    assert result["next_node"] == "run_dataframe_analysis", "Should be case-insensitive."


def test_run_dataframe_analysis_node():
    """
    Tests the run_dataframe_analysis_node with a sample DataFrame and a question.
    Checks if the text answer is present, status is 'ok', and the chart (if any) is valid.
    """
    data = {
        "Product": ["A", "B", "C", "D", "E"],
        "Price": [10.0, 20.0, 30.0, 40.0, 50.0],
        "Quantity": [1, 2, 3, 4, 5],
    }
    df = pd.DataFrame(data)
    input_data = {
        "df": df,
        "question": "What is the average of the Price column?"
    }
    result = run_dataframe_analysis_node(input_data)
    assert result["status"] == "ok", f"Status should be 'ok', got: {result['status']} ({result['message']})"
    assert isinstance(result["text_answer"], str) and result["text_answer"].strip() != "", "Text answer should not be empty."
    assert re.search(r"\d", result["text_answer"]), "The answer should contain a number."
    if result["chart_base64"] is not None:
        assert isinstance(result["chart_base64"], str), "Chart should be a base64 string."
        assert result["chart_base64"].startswith("data:image") or result["chart_base64"].startswith("iVBOR"), "Chart should be a valid base64 image." 