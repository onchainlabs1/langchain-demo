#!/usr/bin/env python3
"""
Demonstration script for the Data Analyst Agent.
This script shows how to use the core functionality programmatically.
"""

import sys
import os
import pandas as pd
import io

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.upload import validate_file_upload
from core.analysis import run_dataframe_analysis
from graph.grafo import build_graph


def demo_csv_analysis():
    """Demonstrate CSV file analysis."""
    print("📊 CSV Analysis Demo")
    print("=" * 50)
    
    # Create sample CSV data
    csv_data = """Date,Region,Product,Sales,Quantity,Profit
2024-01-01,North,Laptop,1200.50,2,240.10
2024-01-02,South,Phone,800.25,3,160.05
2024-01-03,East,Tablet,600.75,1,120.15
2024-01-04,West,Laptop,1100.00,2,220.00
2024-01-05,North,Phone,750.30,2,150.06"""
    
    # Create file-like object
    csv_file = io.StringIO(csv_data)
    csv_file.name = "sample_data.csv"
    
    try:
        # Validate and load the file
        df = validate_file_upload(csv_file)
        print(f"✅ File loaded successfully! Shape: {df.shape}")
        print(f"📋 Columns: {list(df.columns)}")
        print()
        
        # Example questions
        questions = [
            "What are the main trends in this dataset?",
            "Show me a summary of sales by region",
            "What is the average profit per transaction?"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"❓ Question {i}: {question}")
            result_text, chart_base64 = run_dataframe_analysis(
                df=df,
                question=question
            )
            print(f"📝 Answer: {result_text}")
            if chart_base64:
                print("📈 Chart generated!")
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_json_analysis():
    """Demonstrate JSON file analysis."""
    print("\n📊 JSON Analysis Demo")
    print("=" * 50)
    
    # Create sample JSON data
    json_data = """[
  {"id": 1, "name": "John Doe", "department": "Engineering", "salary": 75000, "age": 32, "experience_years": 5, "performance_score": 8.5},
  {"id": 2, "name": "Jane Smith", "department": "Marketing", "salary": 65000, "age": 28, "experience_years": 3, "performance_score": 9.2},
  {"id": 3, "name": "Bob Johnson", "department": "Sales", "salary": 70000, "age": 35, "experience_years": 7, "performance_score": 7.8},
  {"id": 4, "name": "Alice Brown", "department": "Engineering", "salary": 80000, "age": 30, "experience_years": 6, "performance_score": 9.0}
]"""
    
    # Create file-like object
    json_file = io.StringIO(json_data)
    json_file.name = "sample_data.json"
    
    try:
        # Validate and load the file
        df = validate_file_upload(json_file)
        print(f"✅ File loaded successfully! Shape: {df.shape}")
        print(f"📋 Columns: {list(df.columns)}")
        print()
        
        # Example questions
        questions = [
            "Which department has the highest average salary?",
            "Show me the correlation between age and performance score",
            "What is the distribution of experience years?"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"❓ Question {i}: {question}")
            result_text, chart_base64 = run_dataframe_analysis(
                df=df,
                question=question
            )
            print(f"📝 Answer: {result_text}")
            if chart_base64:
                print("📈 Chart generated!")
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Error: {e}")


def demo_langgraph():
    """Demonstrate LangGraph functionality."""
    print("\n🔄 LangGraph Demo")
    print("=" * 50)
    
    # Create sample data
    df = pd.DataFrame({
        "Product": ["A", "B", "C", "D"],
        "Price": [10.0, 20.0, 30.0, 40.0],
        "Quantity": [1, 2, 3, 4]
    })
    
    try:
        # Build and run the graph
        graph = build_graph()
        
        # Test different types of questions
        test_cases = [
            {
                "question": "What is the average price?",
                "description": "Data analysis question"
            },
            {
                "question": "What is the capital of France?",
                "description": "Non-data question"
            }
        ]
        
        for test_case in test_cases:
            print(f"❓ {test_case['description']}: {test_case['question']}")
            
            initial_state = {
                "df": df,
                "question": test_case["question"],
                "next_node": "",
                "text_answer": "",
                "chart_base64": None,
                "status": "",
                "message": ""
            }
            
            result = graph.invoke(initial_state)
            print(f"📝 Answer: {result['text_answer']}")
            print(f"🔄 Next Node: {result['next_node']}")
            print(f"✅ Status: {result['status']}")
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all demonstrations."""
    print("🚀 Data Analyst Agent - Demonstration")
    print("=" * 60)
    print("This script demonstrates the core functionality of the")
    print("Data Analyst Agent using sample data and questions.")
    print()
    
    # Run demonstrations
    demo_csv_analysis()
    demo_json_analysis()
    demo_langgraph()
    
    print("\n🎉 Demonstration completed!")
    print("\n💡 To use the web interface, run:")
    print("   python run_app.py")
    print("   Then open http://localhost:8501 in your browser")


if __name__ == "__main__":
    main() 