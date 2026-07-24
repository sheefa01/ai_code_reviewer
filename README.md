# AI-Powered Python Code Reviewer
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Groq](https://img.shields.io/badge/AI-Groq_Llama_3-orange)
A robust, AI-powered CLI tool to review Python code for security, performance, and best practices.

## Project Structure
- `src/main.py`: The Command Line Interface.
- `src/app.py`: The Streamlit Web Dashboard.
- `tests/`: Unit and integration tests.
- `requirements.txt`: Project dependencies.
- `setup.py`: Script to install the tool globally.

## Prerequisites

- Python 3.8+
- A free API key from [Groq Console](https://console.groq.com/keys)

## Installation

You can install this tool globally on your system, allowing you to run it from any directory.

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/ai_code_reviewer.git
   cd ai_code_reviewer
   ```

2. Copy the example environment file and add your Groq API key:
   ```bash
   cp .env.example .env
   # Edit .env and paste your API key
   ```

3. Install the tool globally:
   ```bash
   pip install -e .
   ```

## Usage

Once installed, you can use the `ai-reviewer` command anywhere on your computer!

### Review a specific file:
```bash
ai-reviewer path/to/your/script.py
```

### Review an entire directory:
```bash
ai-reviewer path/to/your/project_folder
```

### Save the review to a file:
You can use the `--output` or `-o` flag to save the beautifully formatted Markdown review directly to a file.
```bash
ai-reviewer path/to/script.py --output report.md
```

## Web Dashboard (Streamlit)

This project also includes a stunning, premium Web Dashboard with a drag-and-drop file uploader!

1. Start the dashboard:
   ```bash
   python -m streamlit run src/app.py
   ```
2. Your browser will automatically open to `http://localhost:8501`.
