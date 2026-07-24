import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class CodeReviewer:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing from environment variables.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
    def review_code(self, file_content: str, filename: str) -> str:
        """
        Sends the code to Gemini and returns the review.
        """
        prompt = f"""
        You are a Senior Python Developer. Review the following code in '{filename}'.
        
        Focus on:
        1. Security vulnerabilities
        2. Performance bottlenecks
        3. Python best practices (PEP 8)
        4. Potential bugs

        Please format your response in clean Markdown.

        Code:
        ```python
        {file_content}
        ```
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error connecting to Gemini API: {e}"
