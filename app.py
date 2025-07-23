import streamlit as st
import pandas as pd
import base64
import io
import sys
import os
from typing import Optional, Tuple

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.upload import validate_file_upload
from graph.grafo import build_graph


def main():
    """
    Main Streamlit application for the Data Analyst Agent.
    Provides a user-friendly interface for data analysis using LangGraph.
    """
    
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
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
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
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">📊 Data Analyst Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Upload your data and ask questions to get intelligent insights</p>', unsafe_allow_html=True)
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This application uses LangChain and LangGraph to provide intelligent data analysis.
        
        **Features:**
        - Multi-format file support
        - Natural language queries
        - Secure data processing
        - Interactive visualizations
        """)
        
        st.markdown("---")
        st.header("📋 Supported Formats")
        st.markdown("""
        - **CSV** files (.csv)
        - **Excel** files (.xlsx, .xls)
        - **JSON** files (.json)
        - **Parquet** files (.parquet)
        """)
        
        st.markdown("---")
        st.header("💡 Example Questions")
        st.markdown("""
        - "What is the average of column X?"
        - "Show me a summary of the data"
        - "What are the main trends?"
        - "Generate statistics for numeric columns"
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.header("📁 Upload Your Data")
        
        # File uploader with caching
        uploaded_file = st.file_uploader(
            "Choose a file to analyze",
            type=['csv', 'xlsx', 'xls', 'json', 'parquet'],
            help="Select a data file to upload and analyze"
        )
        
        # Display file info if uploaded
        if uploaded_file is not None:
            try:
                # Use cache to avoid reloading the same file
                @st.cache_data
                def load_data(file):
                    """Load and validate uploaded file data."""
                    return validate_file_upload(file)
                
                df = load_data(uploaded_file)
                
                st.success(f"✅ File uploaded successfully!")
                st.info(f"**Dataset Info:** {df.shape[0]} rows × {df.shape[1]} columns")
                
                # Show data preview
                with st.expander("📋 Data Preview"):
                    st.dataframe(df.head(10), use_container_width=True)
                    st.write(f"**Columns:** {', '.join(df.columns)}")
                    
                    # Show data types
                    dtype_info = df.dtypes.to_dict()
                    st.write("**Data Types:**")
                    for col, dtype in dtype_info.items():
                        st.write(f"- {col}: {dtype}")
                
            except Exception as e:
                st.error(f"❌ Error uploading file: {str(e)}")
                st.info("💡 Please check the file format and try again.")
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
            height=120,
            placeholder="e.g., What is the average of the Sales column? Show me a summary of the data. What are the main trends?",
            help="Ask any question about your data in natural language"
        )
        
        # Analysis button
        analyze_button = st.button(
            "🚀 Analyze Data",
            type="primary",
            disabled=df is None or not question.strip(),
            help="Click to analyze your data with the uploaded question"
        )
        
        if df is None or not question.strip():
            if df is None:
                st.warning("⚠️ Please upload a file first")
            elif not question.strip():
                st.warning("⚠️ Please enter a question")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Analysis results section
    if analyze_button and df is not None and question.strip():
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.header("📊 Analysis Results")
        
        # Show spinner during analysis
        with st.spinner("🔍 Analyzing your data with LangGraph..."):
            try:
                # Build and run the LangGraph
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
                
                # Execute the analysis
                result = graph.invoke(initial_state)
                
                # Display results
                if result["status"] == "ok":
                    st.success("✅ Analysis completed successfully!")
                    
                    # Display text answer
                    st.subheader("📝 Analysis Summary")
                    st.write(result["text_answer"])
                    
                    # Display chart if available
                    if result["chart_base64"]:
                        st.subheader("📈 Visualization")
                        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                        
                        try:
                            # Decode and display chart
                            chart_data = base64.b64decode(result["chart_base64"])
                            st.image(chart_data, use_column_width=True, caption="Generated Chart")
                        except Exception as e:
                            st.error(f"Error displaying chart: {str(e)}")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Show additional info
                    with st.expander("🔍 Analysis Details"):
                        st.write(f"**Status:** {result['status']}")
                        st.write(f"**Message:** {result['message']}")
                        st.write(f"**Next Node:** {result['next_node']}")
                
                else:
                    st.error(f"❌ Analysis failed: {result['message']}")
                    st.info("💡 Try rephrasing your question or uploading a different file")
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
                st.info("💡 Please check your data and question, then try again")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
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