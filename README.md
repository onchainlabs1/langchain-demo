# Data Analyst Agent

A secure Data Analyst Agent built with LangChain, LangGraph, and Streamlit, featuring TDD practices and comprehensive security measures.

## 🚀 Features

- **Secure Data Analysis**: Safe execution environment with code validation
- **Multi-format Support**: CSV, Excel, JSON, and Parquet files
- **Natural Language Queries**: Ask questions in plain English
- **Interactive Visualizations**: Charts and graphs with matplotlib
- **LangGraph Integration**: Intelligent routing and workflow management
- **Web Interface**: Beautiful Streamlit UI with modern design
- **Comprehensive Testing**: TDD approach with 73% test coverage
- **Security First**: Sandbox execution, input validation, and timeout protection

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/onchainlabs1/langchain-demo.git
   cd langchain-demo
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```

3. **Run tests to verify installation:**
   ```bash
   pytest tests/ -v --cov=src
   ```

## 🚀 Quick Start

### Running the Web Application

1. **Start the Streamlit app:**
   ```bash
   python run_app.py
   ```
   
   Or directly with Streamlit:
   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**
   Navigate to `http://localhost:8501`

3. **Upload data and ask questions:**
   - Upload CSV, Excel, JSON, or Parquet files
   - Type natural language questions
   - Get instant analysis and visualizations

### Using the API

```python
from src.core.upload import validate_file_upload
from src.core.analysis import execute_dataframe_analysis
from src.graph.grafo import build_graph

# Upload and validate a file
df = validate_file_upload(uploaded_file)

# Execute analysis
result_text, chart_base64 = execute_dataframe_analysis(
    df=df,
    question="What are the main trends in this dataset?",
    security_level="High",
    max_execution_time=30
)

# Build and run LangGraph
graph = build_graph()
result = graph.invoke({"question": "Analyze this data", "dataframe": df})
```

## 🧪 Testing

Run the complete test suite:
```bash
pytest tests/ -v --cov=src
```

### Test Coverage
- **File Upload Validation**: 100%
- **DataFrame Analysis**: 100%
- **LangGraph Nodes**: 100%
- **Graph Construction**: 100%
- **Overall Coverage**: 73%

## 🔒 Security Features

- **Code Validation**: All generated code is validated before execution
- **Sandbox Execution**: Secure environment using Pyodide
- **Input Sanitization**: User inputs are cleaned and validated
- **Timeout Protection**: Analysis is limited by time constraints
- **File Validation**: Uploaded files are checked for safety

## 📁 Project Structure

```
langchain/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── upload.py          # File upload validation
│   │   └── analysis.py        # Secure DataFrame analysis
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── nos.py             # LangGraph nodes
│   │   └── grafo.py           # Graph construction
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_upload.py         # Upload validation tests
│   ├── test_analysis.py       # Analysis function tests
│   ├── test_nos.py            # Node tests
│   └── test_grafo.py          # Graph tests
├── data/                      # Sample data files
│   ├── sample_data.csv        # Sales data
│   └── sample_data.json       # Employee data
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── app.py                     # Main Streamlit application
├── run_app.py                 # Application runner script
├── pyproject.toml             # Project configuration
├── README.md                  # This file
├── USAGE.md                   # Detailed usage guide
└── LICENSE                    # MIT License
```

## 🎯 Example Questions

- "What are the main trends in this dataset?"
- "Show me a correlation analysis between numeric columns"
- "Create a visualization of sales by region"
- "What are the top 5 values in each column?"
- "Generate summary statistics for the dataset"
- "Are there any missing values or outliers?"

## 🔧 Configuration

### Security Levels

- **High**: Maximum restrictions, safe for untrusted data
- **Medium**: Balanced security and functionality
- **Low**: Minimal restrictions, for trusted environments

### Execution Timeouts

- Default: 30 seconds
- Range: 5-60 seconds
- Configurable per analysis request

## 📊 Sample Data

The project includes sample datasets for testing:

- `data/sample_data.csv`: Sales data with regions, products, and metrics
- `data/sample_data.json`: Employee data with departments and performance metrics

## 🌐 Web Interface Features

- **Modern UI**: Clean, responsive design with custom CSS
- **File Upload**: Drag-and-drop support for multiple formats
- **Real-time Preview**: Instant data preview and validation
- **Interactive Settings**: Configurable security and analysis options
- **Visual Results**: Charts and graphs with base64 encoding
- **Error Handling**: User-friendly error messages and suggestions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- LangChain for the AI framework
- LangGraph for workflow management
- Streamlit for the web interface
- Pyodide for secure code execution
- The open-source community for inspiration and tools

---

> All content in this project is in English, including code, comments, and documentation.
