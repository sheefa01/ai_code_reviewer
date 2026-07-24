import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class CodeReviewer:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing from environment variables.")
        
        self.client = Groq(api_key=api_key)
        self.model_name = 'llama3-8b-8192'
        
    def review_code(self, file_content: str, filename: str) -> str:
        """
        Sends the code to Groq (Llama 3) and returns the review.
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
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_name,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error connecting to Groq API: {e}"
