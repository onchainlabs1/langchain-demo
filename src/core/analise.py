import base64
import io
import ast
from typing import Tuple, Optional
import pandas as pd

from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_sandbox.executors import PyodideExecutor
from langgraph.graph import StateGraph, END

# Replace with your preferred LLM and secure configuration
from langchain_openai import ChatOpenAI

def run_dataframe_analysis(
    df: pd.DataFrame, 
    question: str
) -> Tuple[str, Optional[str]]:
    """
    Securely runs an analysis on a DataFrame based on a natural language question,
    using LangChain, LangGraph, and Pyodide sandbox for Python code execution.

    Args:
        df (pd.DataFrame): DataFrame with the data to be analyzed.
        question (str): User's question in Portuguese.

    Returns:
        Tuple[str, Optional[str]]: 
            - Textual answer in Portuguese.
            - Chart image in base64 (if generated), or None.
    """
    # 1. Prepare context for the LLM
    context = f"""
    You are a data analyst. Answer the user's question about the provided DataFrame.
    Generate SAFE Python code for analysis, using only pandas, matplotlib, or altair.
    Never access the network, files, or system commands.
    The DataFrame is available as 'df'.
    Question: {question}
    """

    # 2. Instantiate the language model (LLM)
    llm: BaseLanguageModel = ChatOpenAI(
        temperature=0.0,
        model="gpt-3.5-turbo",  # or another secure model
        streaming=False
    )

    # 3. Generate the Python code for analysis
    prompt = ChatPromptTemplate.from_messages([
        ("system", context),
        ("user", "Generate only the necessary Python code to answer the question, no explanations.")
    ])
    generated_code = llm.invoke(prompt).content.strip()

    # 4. Validate the generated code (forbid dangerous commands)
    try:
        tree = ast.parse(generated_code, mode="exec")
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                # Allow only pandas, matplotlib, altair imports
                names = [alias.name for alias in getattr(node, 'names', [])]
                if any(mod not in ("pandas", "matplotlib", "altair", "pyplot") for mod in names):
                    raise ValueError("Module import not allowed.")
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in ("open", "exec", "eval", "compile", "os", "sys", "subprocess"):
                    raise ValueError("Prohibited function usage detected.")
    except Exception as e:
        return (f"Security error validating generated code: {e}", None)

    # 5. Execute the code in a secure sandbox (Pyodide)
    executor = PyodideExecutor(
        allowed_imports=["pandas", "matplotlib", "altair"],
        disable_network=True,
        cpu_time_limit=5,
        memory_limit_mb=128
    )
    local_vars = {"df": df}
    text_answer = ""
    image_base64 = None

    try:
        # Redirect chart output to buffer
        exec_code = (
            "import matplotlib.pyplot as plt\n"
            "import altair as alt\n"
            "import io, base64\n"
            "buffer = io.BytesIO()\n"
            + generated_code +
            "\nif 'plt' in locals() and plt.get_fignums():\n"
            "    plt.savefig(buffer, format='png')\n"
            "    buffer.seek(0)\n"
            "    img_b64 = 'data:image/png;base64,' + base64.b64encode(buffer.read()).decode('utf-8')\n"
            "    answer = locals().get('answer', '')\n"
            "else:\n"
            "    img_b64 = None\n"
            "    answer = locals().get('answer', '')\n"
        )
        result = executor.execute(exec_code, local_vars=local_vars)
        text_answer = result.get("answer", "").strip() or "Analysis completed."
        image_base64 = result.get("img_b64", None)
    except Exception as e:
        text_answer = f"An error occurred while running the analysis: {e}"
        image_base64 = None

    return text_answer, image_base64 