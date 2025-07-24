"""
Data Analyst Agent - Streamlit Interface

How to run:
    streamlit run app.py

This app allows users to upload a dataset (CSV, Excel, JSON, Parquet), ask a question in English, and receive an answer (text and chart) from the agent using LangGraph.
"""

import streamlit as st
import pandas as pd
import base64
import io
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.upload import validate_file_upload
from graph.grafo import build_graph
from core.analysis import run_dataframe_analysis as executar_analise_dataframe

# Example questions for selectbox
EXAMPLE_QUESTIONS = [
    "What is the average price?",
    "Which region has the highest sales?",
    "How many properties have 3 bedrooms?",
    "What is the total revenue by category?"
]

# Supported file types
FILE_TYPES = ["csv", "xlsx", "json", "parquet"]

# Streamlit app
st.set_page_config(
    page_title="Data Analyst Agent",
    page_icon="📊",
    layout="wide"
)

# --- Header ---
st.title("📊 Data Analyst Agent")
st.markdown("""
A secure, intelligent agent for data analysis. Upload your dataset, ask a question in English, and get instant insights with text and charts.
""")

# --- Example question selectbox ---
st.markdown("**Choose an example question or type your own below:**")
selected_example = st.selectbox(
    "Example questions:",
    EXAMPLE_QUESTIONS,
    index=0,
    key="example_selectbox"
)

# --- File uploader ---
st.markdown("**Upload your dataset:**")
uploaded_file = st.file_uploader(
    "Choose a file",
    type=FILE_TYPES,
    help="Supported formats: CSV, Excel (.xlsx), JSON, Parquet"
)

# --- DataFrame preview and caching ---
def load_and_validate(file):
    """Load and validate the uploaded file, returning a DataFrame."""
    return validate_file_upload(file)

# Use Streamlit cache to avoid reloading the same file
@st.cache_data(show_spinner=False)
def get_dataframe(file):
    return load_and_validate(file)

# Initialize variables
df = None
file_error = None

if uploaded_file is not None:
    try:
        df = get_dataframe(uploaded_file)
        st.success(f"File loaded successfully! Shape: {df.shape[0]} rows × {df.shape[1]} columns.")
        with st.expander("Preview data (first 10 rows)"):
            st.dataframe(df.head(10), use_container_width=True)
    except Exception as e:
        file_error = str(e)
        st.error(f"Error loading file: {file_error}")

# --- Question input ---
st.markdown("**Type your question in English:**")
question = st.text_input(
    "Question:",
    value=selected_example if selected_example else "",
    key="question_input"
)

# --- Analyze button ---
run_analysis = st.button("Analyze Data", type="primary", disabled=(df is None or not question.strip()))

# --- Analysis and results ---
if run_analysis:
    if df is None:
        st.error("Please upload a valid file before analyzing.")
    elif not question.strip():
        st.error("Please enter a question.")
    else:
        with st.spinner("Analyzing your data, please wait..."):
            try:
                # Build the LangGraph
                graph = build_graph()
                # Prepare initial state for the graph
                initial_state = {
                    "df": df,
                    "question": question,
                    "next_node": "",
                    "text_answer": "",
                    "chart_base64": None,
                    "status": "",
                    "message": ""
                }
                # Run the analysis using the graph
                result = graph.invoke(initial_state)
                # --- Display results ---
                if result.get("status") == "ok":
                    st.success("Analysis completed successfully!")
                    st.markdown("**Answer:**")
                    st.write(result.get("text_answer", "No answer returned."))
                    # Display chart if available
                    if result.get("chart_base64"):
                        st.markdown("**Chart:**")
                        try:
                            chart_data = base64.b64decode(result["chart_base64"])
                            st.image(chart_data, use_column_width=True)
                        except Exception as e:
                            st.error(f"Error displaying chart: {e}")
                else:
                    st.error(f"Analysis failed: {result.get('message', 'Unknown error')}")
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")

# --- Footer ---
st.markdown("---")
st.markdown("""
<small>To run this app, use <code>streamlit run app.py</code> in your terminal.</small>
""", unsafe_allow_html=True) 