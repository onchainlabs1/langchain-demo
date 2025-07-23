#!/usr/bin/env python3
"""
Quick test script to verify the Streamlit interface functionality.
This script tests the core components without running the full Streamlit app.
"""

import sys
import os
import pandas as pd
import io

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.upload import validate_file_upload
from graph.grafo import build_graph


def test_file_upload():
    """Test file upload functionality."""
    print("🧪 Testing file upload...")
    
    # Create sample CSV data
    csv_data = """Date,Region,Product,Sales,Quantity,Profit
2024-01-01,North,Laptop,1200.50,2,240.10
2024-01-02,South,Phone,800.25,3,160.05
2024-01-03,East,Tablet,600.75,1,120.15"""
    
    # Create file-like object
    csv_file = io.StringIO(csv_data)
    csv_file.name = "test_data.csv"
    
    try:
        df = validate_file_upload(csv_file)
        print(f"✅ File upload test passed! Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"❌ File upload test failed: {e}")
        return None


def test_langgraph_analysis(df):
    """Test LangGraph analysis functionality."""
    print("🧪 Testing LangGraph analysis...")
    
    if df is None:
        print("❌ Cannot test analysis without DataFrame")
        return
    
    try:
        # Build graph
        graph = build_graph()
        
        # Test question
        question = "What is the average sales?"
        
        # Prepare state
        initial_state = {
            "df": df,
            "question": question,
            "next_node": "",
            "text_answer": "",
            "chart_base64": None,
            "status": "",
            "message": ""
        }
        
        # Execute analysis
        result = graph.invoke(initial_state)
        
        print(f"✅ LangGraph analysis test passed!")
        print(f"   Status: {result['status']}")
        print(f"   Answer: {result['text_answer'][:100]}...")
        
    except Exception as e:
        print(f"❌ LangGraph analysis test failed: {e}")


def test_interface_components():
    """Test interface components."""
    print("🧪 Testing interface components...")
    
    try:
        # Test imports
        import streamlit as st
        print("✅ Streamlit import successful")
        
        # Test app import
        import app
        print("✅ App module import successful")
        
        # Test main function exists
        if hasattr(app, 'main'):
            print("✅ Main function found")
        else:
            print("❌ Main function not found")
            
    except Exception as e:
        print(f"❌ Interface component test failed: {e}")


def main():
    """Run all interface tests."""
    print("🚀 Testing Data Analyst Agent Interface")
    print("=" * 50)
    
    # Test interface components
    test_interface_components()
    print()
    
    # Test file upload
    df = test_file_upload()
    print()
    
    # Test analysis
    if df is not None:
        test_langgraph_analysis(df)
    
    print()
    print("🎉 Interface tests completed!")
    print()
    print("💡 To run the full application:")
    print("   streamlit run app.py")
    print("   or")
    print("   python run_app.py")


if __name__ == "__main__":
    main() 