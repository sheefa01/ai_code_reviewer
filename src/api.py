from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
from src.ai.reviewer import CodeReviewer

app = FastAPI(
    title="AI Python Code Reviewer API",
    description="Upload a Python file and get an AI-powered code review.",
    version="1.0.0"
)

# Initialize reviewer
try:
    reviewer = CodeReviewer()
except ValueError as e:
    print(f"Warning: Configuration Error - {e}")
    reviewer = None

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>AI Code Reviewer</title>
            <style>
                body { font-family: sans-serif; text-align: center; margin-top: 50px; background-color: #121212; color: white; }
                a { color: #bb86fc; text-decoration: none; font-size: 1.2rem; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>Welcome to the AI Code Reviewer API! 🚀</h1>
            <p>The system is running perfectly.</p>
            <br/>
            <a href="/docs">Click here to open the Interactive Web UI (Swagger) -></a>
        </body>
    </html>
    """

@app.post("/review")
async def review_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.py'):
        raise HTTPException(status_code=400, detail="Only Python (.py) files are supported.")
    
    if reviewer is None:
        raise HTTPException(status_code=500, detail="AI Reviewer is not configured. Check your .env file.")

    content = await file.read()
    code_text = content.decode("utf-8")
    
    feedback = reviewer.review_code(code_text, file.filename)
    
    return {
        "filename": file.filename,
        "status": "success",
        "review_markdown": feedback
    }

if __name__ == "__main__":
    uvicorn.run("src.api:app", host="127.0.0.1", port=8000, reload=True)
