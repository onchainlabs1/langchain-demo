import pytest
import pandas as pd
import re
from core.analysis import run_dataframe_analysis


def test_run_dataframe_analysis():
    """
    Tests the run_dataframe_analysis function with a simple DataFrame and a question about the average price.
    Checks if the answer is in English, contains a number, and if the chart (if any) is in base64.
    """
    # 1. Create sample DataFrame
    data = {
        "Product": ["A", "B", "C", "D", "E"],
        "Price": [10.0, 20.0, 30.0, 40.0, 50.0],
        "Quantity": [1, 2, 3, 4, 5],
    }
    df = pd.DataFrame(data)

    # 2. Question in English
    question = "What is the average of the Price column?"

    # 3. Call the analysis function
    try:
        answer, chart_base64 = run_dataframe_analysis(df, question)
    except Exception as e:
        pytest.fail(f"Error running analysis: {e}")

    # 4. Checks
    assert isinstance(answer, str), "The answer should be a string."
    assert answer.strip() != "", "The answer should not be empty."
    assert re.search(r"\d", answer), "The answer should contain a number."
    assert any(word in answer.lower() for word in ["average", "price"]), "The answer should mention 'average' or 'price'."

    if chart_base64 is not None:
        assert isinstance(chart_base64, str), "The chart should be a base64 string."
        assert chart_base64.startswith("data:image") or chart_base64.startswith("iVBOR"), "The chart should be a valid base64 image."

    # 5. Success message
    print("DataFrame analysis test executed successfully.") 