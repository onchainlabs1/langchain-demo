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

# Example questions for regular datasets
EXAMPLE_QUESTIONS = [
    "What is the average price?",
    "Which region has the highest sales?",
    "How many properties have 3 bedrooms?",
    "What is the total revenue by category?"
]

# Health insurance demo questions
INSURANCE_QUESTIONS = [
    "What is the average charge per region?",
    "Do smokers pay more than non-smokers?",
    "Show the relation between BMI and charges",
    "What is the average charge by age group?",
    "Which region has the lowest average cost?"
]

# Supported file types
FILE_TYPES = ["csv", "xlsx", "json", "parquet"]

# Streamlit app configuration
st.set_page_config(
    page_title="Data Analyst Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 2rem;
}
.demo-section {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 5px solid #667eea;
    margin: 1rem 0;
}
.suggestions-box {
    background-color: #e3f2fd;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #2196f3;
    margin: 1rem 0;
}
.upload-section {
    background-color: #f5f5f5;
    padding: 1.5rem;
    border-radius: 10px;
    border: 2px dashed #ccc;
    text-align: center;
}
.result-container {
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# === VISUAL HEADER ===
st.markdown("""
<div class="main-header">
    <h1>📊 Data Analyst Agent</h1>
    <p><em>"Ask anything about your dataset. Get insights instantly — no code required."</em></p>
</div>
""", unsafe_allow_html=True)

# === SESSION STATE INITIALIZATION ===
if "demo_df" not in st.session_state:
    st.session_state.demo_df = None
if "demo_question" not in st.session_state:
    st.session_state.demo_question = ""
if "is_demo_loaded" not in st.session_state:
    st.session_state.is_demo_loaded = False

# === DEMO DATA SECTION ===
st.markdown('<div class="demo-section">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**🚀 Quick Start: Try our demo dataset**")
    st.markdown("Explore health insurance data with pre-built questions")
with col2:
    demo_clicked = st.button("📂 Load demo data (health insurance)", key="demo_button", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)

# === DEMO DATA LOADING LOGIC ===
df = None
file_error = None
is_demo = False

if demo_clicked:
    try:
        demo_path = os.path.join("data", "insurance.csv")
        if not os.path.exists(demo_path):
            st.session_state.demo_df = None
            st.session_state.is_demo_loaded = False
            st.warning("⚠️ Demo file 'data/insurance.csv' not found. Please add the file to the data folder.")
        else:
            demo_df = pd.read_csv(demo_path)
            st.session_state.demo_df = demo_df
            st.session_state.demo_question = INSURANCE_QUESTIONS[0]
            st.session_state.is_demo_loaded = True
            is_demo = True
            st.success("✅ Demo dataset loaded successfully!")
    except Exception as e:
        st.session_state.demo_df = None
        st.session_state.is_demo_loaded = False
        st.error(f"❌ Could not load demo data: {e}")

# Use demo data if loaded
if st.session_state.demo_df is not None and st.session_state.is_demo_loaded:
    df = st.session_state.demo_df.copy()
    is_demo = True

# === MAIN CONTENT AREA ===
col1, col2 = st.columns([1, 1])

with col1:
    # === FILE UPLOAD SECTION ===
    st.markdown("### 📁 Upload your dataset")
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file to analyze",
        type=FILE_TYPES,
        help="Supported formats: CSV, Excel (.xlsx), JSON, Parquet",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None and not is_demo:
        try:
            @st.cache_data(show_spinner=False)
            def get_dataframe(file):
                return validate_file_upload(file)
            
            df = get_dataframe(uploaded_file)
            st.success(f"✅ File loaded! {df.shape[0]} rows × {df.shape[1]} columns")
            st.session_state.is_demo_loaded = False  # Reset demo when new file uploaded
        except Exception as e:
            file_error = str(e)
            st.error(f"❌ Error loading file: {file_error}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # === DATA PREVIEW ===
    if df is not None:
        with st.expander("👀 Preview data (first 10 rows)", expanded=False):
            st.dataframe(df.head(10), use_container_width=True)
            st.caption(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")

with col2:
    # === QUESTION SECTION ===
    st.markdown("### ❓ Ask your question")
    
    # Show suggestions for demo data
    if is_demo:
        st.markdown("""
        <div class="suggestions-box">
        <strong>💡 Try questions like:</strong><br>
        • <em>What is the average charge by region?</em><br>
        • <em>Do smokers pay more than non-smokers?</em><br>
        • <em>What is the relation between BMI and charges?</em>
        </div>
        """, unsafe_allow_html=True)
        
        selected_example = st.selectbox(
            "Health insurance questions:",
            INSURANCE_QUESTIONS,
            index=INSURANCE_QUESTIONS.index(st.session_state.demo_question) if st.session_state.demo_question in INSURANCE_QUESTIONS else 0,
            key="insurance_example_selectbox"
        )
        st.session_state.demo_question = selected_example
        
        question = st.text_area(
            "Your question:",
            value=st.session_state.demo_question,
            height=80,
            key="question_input_demo"
        )
    else:
        st.markdown("""
        <div class="suggestions-box">
        <strong>💡 Try questions like:</strong><br>
        • <em>What is the average price?</em><br>
        • <em>Which region has the highest sales?</em><br>
        • <em>Show me a summary of the data</em>
        </div>
        """, unsafe_allow_html=True)
        
        selected_example = st.selectbox(
            "Example questions:",
            EXAMPLE_QUESTIONS,
            index=0,
            key="example_selectbox"
        )
        
        question = st.text_area(
            "Your question:",
            value=selected_example if selected_example else "",
            height=80,
            key="question_input"
        )

# === ANALYZE BUTTON ===
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if df is None or not question.strip():
        if df is None:
            st.warning("⚠️ Please upload a file or load the demo dataset first.")
        elif not question.strip():
            st.warning("⚠️ Please enter a question to analyze.")
        
        analyze_button = st.button("📈 Analyze Data", disabled=True, use_container_width=True)
    else:
        analyze_button = st.button("📈 Analyze Data", type="primary", use_container_width=True)

# === ANALYSIS AND RESULTS ===
if analyze_button and df is not None and question.strip():
    with st.spinner("🔍 Analyzing with our agent..."):
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
            
            # === DISPLAY RESULTS ===
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            
            if result.get("status") == "ok":
                st.success("✅ Analysis completed!")
                
                # Display the question asked
                st.markdown(f"**Question:** _{question}_")
                st.markdown("---")
                
                # Display text answer
                st.markdown("### 📝 Analysis Results")
                answer_text = result.get("text_answer", "No answer returned.")
                st.markdown(f"**Answer:** {answer_text}")
                
                # Display chart if available
                if result.get("chart_base64"):
                    st.markdown("### 📊 Visualization")
                    try:
                        chart_data = base64.b64decode(result["chart_base64"])
                        st.image(chart_data, use_column_width=True, caption="Generated visualization")
                    except Exception as e:
                        st.error(f"❌ Error displaying chart: {e}")
                
                # Show dataset info again for context
                if df is not None:
                    with st.expander("📋 Dataset context", expanded=False):
                        st.write(f"**Analyzed dataset:** {df.shape[0]} rows, {df.shape[1]} columns")
                        st.write(f"**Columns:** {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
                
            else:
                st.error(f"❌ Analysis failed: {result.get('message', 'Unknown error')}")
                st.info("💡 Try rephrasing your question or check your dataset.")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ An error occurred during analysis: {e}")
            st.info("💡 Please check your data and question, then try again.")

# === FOOTER ===
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🔒 Built with <strong>LangChain</strong>, <strong>LangGraph</strong>, and <strong>Streamlit</strong></p>
    <p><small>To run this app locally: <code>streamlit run app.py</code></small></p>
</div>
""", unsafe_allow_html=True) 