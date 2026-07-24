from setuptools import setup, find_packages

setup(
    name="ai-code-reviewer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "groq>=0.4.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ai-reviewer=src.main:app",
        ],
    },
    author="sheefa01",
    description="An AI-powered Python code reviewer CLI using Groq Llama 3.",
)
