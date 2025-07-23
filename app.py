import streamlit as st
import pandas as pd
import io
import base64
from typing import Optional, Tuple
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.analysis import execute_dataframe_analysis
from graph.grafo import build_graph
from core.upload import validate_file_upload


def main():
    """Main Streamlit application for the Data Analyst Agent."""
    
    # Page configuration
    st.set_page_config(
        page_title="Data Analyst Agent",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
        margin: 1rem 0;
    }
    .result-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    .chart-container {
        text-align: center;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">📊 Data Analyst Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload your data and ask questions to get intelligent insights</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Analysis type selection
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Basic Analysis", "Statistical Analysis", "Visualization", "Custom Query"],
            help="Choose the type of analysis you want to perform"
        )
        
        # Security level
        security_level = st.selectbox(
            "Security Level",
            ["High", "Medium", "Low"],
            index=0,
            help="Higher security means more restrictions on code execution"
        )
        
        # Max execution time
        max_execution_time = st.slider(
            "Max Execution Time (seconds)",
            min_value=5,
            max_value=60,
            value=30,
            help="Maximum time allowed for analysis execution"
        )
        
        st.markdown("---")
        st.markdown("### 📋 Supported Formats")
        st.markdown("- CSV files")
        st.markdown("- Excel files (.xlsx, .xls)")
        st.markdown("- JSON files")
        st.markdown("- Parquet files")
        
        st.markdown("---")
        st.markdown("### 🔒 Security Features")
        st.markdown("- Code validation")
        st.markdown("- Sandbox execution")
        st.markdown("- Input sanitization")
        st.markdown("- Timeout protection")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.header("📁 Upload Your Data")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx', 'xls', 'json', 'parquet'],
            help="Upload your dataset for analysis"
        )
        
        if uploaded_file is not None:
            # Validate file upload
            try:
                df = validate_file_upload(uploaded_file)
                st.success(f"✅ File uploaded successfully! Shape: {df.shape}")
                
                # Show data preview
                with st.expander("📋 Data Preview"):
                    st.dataframe(df.head(10))
                    st.write(f"**Columns:** {list(df.columns)}")
                    st.write(f"**Data Types:** {dict(df.dtypes)}")
                
            except Exception as e:
                st.error(f"❌ Error uploading file: {str(e)}")
                df = None
        else:
            df = None
            st.info("👆 Please upload a file to begin analysis")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.header("❓ Ask Your Question")
        
        # Question input
        question = st.text_area(
            "What would you like to know about your data?",
            height=150,
            placeholder="e.g., What are the main trends in this dataset? Show me a correlation analysis. Create a visualization of sales by region.",
            help="Ask any question about your data"
        )
        
        # Example questions
        with st.expander("💡 Example Questions"):
            st.markdown("""
            - What are the main trends in this dataset?
            - Show me a correlation analysis between numeric columns
            - Create a visualization of sales by region
            - What are the top 5 values in each column?
            - Generate summary statistics for the dataset
            - Are there any missing values or outliers?
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis execution
    if st.button("🚀 Run Analysis", type="primary", disabled=df is None or not question.strip()):
        st.warning("Please upload a file and enter a question to run analysis")
    
    if df is not None and question.strip() and st.button("🚀 Run Analysis", type="primary"):
        with st.spinner("🔍 Analyzing your data..."):
            try:
                # Execute analysis
                result_text, chart_base64 = execute_dataframe_analysis(
                    df=df,
                    question=question,
                    security_level=security_level,
                    max_execution_time=max_execution_time
                )
                
                # Display results
                st.markdown('<div class="result-section">', unsafe_allow_html=True)
                st.header("📊 Analysis Results")
                
                # Text results
                st.subheader("📝 Analysis Summary")
                st.write(result_text)
                
                # Chart if available
                if chart_base64:
                    st.subheader("📈 Visualization")
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    
                    # Decode and display chart
                    chart_data = base64.b64decode(chart_base64)
                    st.image(chart_data, use_column_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.info("💡 Try rephrasing your question or uploading a different file")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🔒 Built with security in mind using LangChain, LangGraph, and Streamlit</p>
        <p>📊 Data Analyst Agent - Portfolio Project</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main() 