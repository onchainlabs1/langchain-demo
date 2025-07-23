# Data Analyst Agent - Usage Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- All dependencies installed (see `pyproject.toml`)

### Running the Application

1. **Install dependencies:**
   ```bash
   pip install -e .
   ```

2. **Run the application:**
   ```bash
   python run_app.py
   ```
   
   Or directly with Streamlit:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:8501`

## 📊 How to Use

### 1. Upload Your Data
- Supported formats: CSV, Excel (.xlsx, .xls), JSON, Parquet
- Click "Browse files" and select your dataset
- The app will validate and preview your data

### 2. Configure Settings (Sidebar)
- **Analysis Type**: Choose the type of analysis you want
- **Security Level**: Set security restrictions (High/Medium/Low)
- **Max Execution Time**: Set timeout for analysis (5-60 seconds)

### 3. Ask Questions
Type natural language questions about your data, such as:
- "What are the main trends in this dataset?"
- "Show me a correlation analysis between numeric columns"
- "Create a visualization of sales by region"
- "What are the top 5 values in each column?"
- "Generate summary statistics for the dataset"
- "Are there any missing values or outliers?"

### 4. View Results
- **Text Analysis**: Detailed insights and findings
- **Visualizations**: Charts and graphs (when applicable)
- **Data Preview**: Quick overview of your dataset

## 🔒 Security Features

The application includes several security measures:

- **Code Validation**: All generated code is validated before execution
- **Sandbox Execution**: Code runs in a secure environment
- **Input Sanitization**: User inputs are cleaned and validated
- **Timeout Protection**: Analysis is limited by time constraints
- **File Validation**: Uploaded files are checked for safety

## 📁 Sample Data

The application includes sample datasets for testing:

- `data/sample_data.csv`: Sales data with regions, products, and metrics
- `data/sample_data.json`: Employee data with departments and performance metrics

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v --cov=src
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the project root directory
2. **Port Already in Use**: Change the port in `run_app.py` or kill existing processes
3. **File Upload Issues**: Check file format and size limits
4. **Analysis Timeout**: Increase the max execution time in settings

### Getting Help

- Check the console output for error messages
- Verify your data format is supported
- Try rephrasing your question
- Use the sample data to test functionality

## 🔧 Advanced Configuration

### Environment Variables
- `STREAMLIT_SERVER_PORT`: Set custom port (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Set server address (default: localhost)

### Custom Themes
Edit `.streamlit/config.toml` to customize the app appearance.

## 📈 Features

- **Multi-format Support**: CSV, Excel, JSON, Parquet
- **Natural Language Queries**: Ask questions in plain English
- **Interactive Visualizations**: Charts and graphs
- **Security First**: Safe code execution
- **Real-time Analysis**: Instant results
- **Responsive Design**: Works on desktop and mobile

## 🎯 Example Workflows

### Sales Analysis
1. Upload sales data (CSV/Excel)
2. Ask: "Show me sales trends by region"
3. Get visualization and insights

### Employee Performance
1. Upload employee data (JSON)
2. Ask: "Which departments have the highest performance scores?"
3. Get analysis and recommendations

### Data Quality Check
1. Upload any dataset
2. Ask: "Are there missing values or outliers?"
3. Get data quality report 