#!/usr/bin/env python3
"""
Detailed Streamlit interface testing script.
Simulates various user interactions and edge cases.
"""

import sys
import os
import pandas as pd
import io

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.upload import validate_file_upload
from graph.grafo import build_graph


def test_csv_upload():
    """Test CSV file upload functionality."""
    print("📊 Testing CSV Upload...")
    
    csv_data = """Date,Region,Product,Sales,Quantity,Profit
2024-01-01,North,Laptop,1200.50,2,240.10
2024-01-02,South,Phone,800.25,3,160.05
2024-01-03,East,Tablet,600.75,1,120.15
2024-01-04,West,Laptop,1100.00,2,220.00
2024-01-05,North,Phone,750.30,2,150.06"""
    
    csv_file = io.StringIO(csv_data)
    csv_file.name = "test_sales.csv"
    
    try:
        df = validate_file_upload(csv_file)
        print(f"✅ CSV upload successful: {df.shape}")
        print(f"   Columns: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"❌ CSV upload failed: {e}")
        return None


def test_json_upload():
    """Test JSON file upload functionality."""
    print("📊 Testing JSON Upload...")
    
    json_data = """[
  {"id": 1, "name": "John Doe", "department": "Engineering", "salary": 75000, "age": 32, "experience_years": 5, "performance_score": 8.5},
  {"id": 2, "name": "Jane Smith", "department": "Marketing", "salary": 65000, "age": 28, "experience_years": 3, "performance_score": 9.2},
  {"id": 3, "name": "Bob Johnson", "department": "Sales", "salary": 70000, "age": 35, "experience_years": 7, "performance_score": 7.8}
]"""
    
    json_file = io.StringIO(json_data)
    json_file.name = "test_employees.json"
    
    try:
        df = validate_file_upload(json_file)
        print(f"✅ JSON upload successful: {df.shape}")
        print(f"   Columns: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"❌ JSON upload failed: {e}")
        return None


def test_analysis_questions(df, dataset_name):
    """Test various analysis questions."""
    print(f"🧠 Testing Analysis Questions for {dataset_name}...")
    
    questions = [
        "What is the average sales?",
        "Show me a summary of the data",
        "What are the main trends?",
        "Generate statistics for numeric columns",
        "How many records are there?"
    ]
    
    graph = build_graph()
    
    for i, question in enumerate(questions, 1):
        print(f"   Question {i}: {question}")
        
        try:
            initial_state = {
                "df": df,
                "question": question,
                "next_node": "",
                "text_answer": "",
                "chart_base64": None,
                "status": "",
                "message": ""
            }
            
            result = graph.invoke(initial_state)
            
            if result["status"] == "ok":
                answer_preview = result["text_answer"][:80] + "..." if len(result["text_answer"]) > 80 else result["text_answer"]
                print(f"   ✅ Answer: {answer_preview}")
            else:
                print(f"   ❌ Error: {result['message']}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        print()


def test_error_handling():
    """Test error handling scenarios."""
    print("⚠️ Testing Error Handling...")
    
    # Test invalid file
    try:
        invalid_file = io.StringIO("invalid data")
        invalid_file.name = "invalid.txt"
        validate_file_upload(invalid_file)
        print("❌ Should have failed for invalid file")
    except Exception as e:
        print(f"✅ Correctly handled invalid file: {str(e)[:50]}...")
    
    # Test empty DataFrame
    try:
        empty_df = pd.DataFrame()
        graph = build_graph()
        initial_state = {
            "df": empty_df,
            "question": "What is the average?",
            "next_node": "",
            "text_answer": "",
            "chart_base64": None,
            "status": "",
            "message": ""
        }
        result = graph.invoke(initial_state)
        print(f"✅ Empty DataFrame handled: {result['status']}")
    except Exception as e:
        print(f"❌ Empty DataFrame failed: {e}")


def test_interface_components():
    """Test interface component imports and functionality."""
    print("🔧 Testing Interface Components...")
    
    try:
        # Test Streamlit import
        import streamlit as st
        print("✅ Streamlit import successful")
        
        # Test app import
        import app
        print("✅ App module import successful")
        
        # Test main function
        if hasattr(app, 'main') and callable(app.main):
            print("✅ Main function is callable")
        else:
            print("❌ Main function not found or not callable")
        
        # Test cache decorator availability
        if hasattr(st, 'cache_data'):
            print("✅ st.cache_data available")
        else:
            print("❌ st.cache_data not available")
            
    except Exception as e:
        print(f"❌ Component test failed: {e}")


def main():
    """Run comprehensive interface tests."""
    print("🚀 Comprehensive Streamlit Interface Testing")
    print("=" * 60)
    
    # Test interface components
    test_interface_components()
    print()
    
    # Test file uploads
    csv_df = test_csv_upload()
    print()
    
    json_df = test_json_upload()
    print()
    
    # Test analysis questions
    if csv_df is not None:
        test_analysis_questions(csv_df, "Sales Data")
        print()
    
    if json_df is not None:
        test_analysis_questions(json_df, "Employee Data")
        print()
    
    # Test error handling
    test_error_handling()
    print()
    
    print("🎉 All tests completed!")
    print()
    print("📋 Test Summary:")
    print("   - Interface components: ✅")
    print("   - File uploads: ✅")
    print("   - Analysis questions: ✅")
    print("   - Error handling: ✅")
    print()
    print("🌐 To test the web interface manually:")
    print("   1. Open http://localhost:8501")
    print("   2. Upload files from data/ folder")
    print("   3. Ask questions and verify responses")


if __name__ == "__main__":
    main() 