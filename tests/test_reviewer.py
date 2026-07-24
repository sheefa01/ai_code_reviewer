import os
import pytest
from unittest.mock import patch, MagicMock
from src.ai.reviewer import CodeReviewer

@patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
@patch("src.ai.reviewer.genai")
def test_reviewer_initialization_success(mock_genai):
    reviewer = CodeReviewer()
    mock_genai.configure.assert_called_once_with(api_key="test_key")
    mock_genai.GenerativeModel.assert_called_once_with('gemini-1.5-pro-latest')

@patch.dict(os.environ, {}, clear=True)
def test_reviewer_initialization_failure():
    with pytest.raises(ValueError, match="GEMINI_API_KEY is missing"):
        CodeReviewer()

@patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
@patch("src.ai.reviewer.genai")
def test_review_code_success(mock_genai):
    # Setup mock
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "This is a great test review."
    mock_model.generate_content.return_value = mock_response
    mock_genai.GenerativeModel.return_value = mock_model
    
    reviewer = CodeReviewer()
    feedback = reviewer.review_code("print('hello')", "test.py")
    
    assert feedback == "This is a great test review."
    mock_model.generate_content.assert_called_once()
    
    # Check if the prompt contains our code and filename
    called_prompt = mock_model.generate_content.call_args[0][0]
    assert "test.py" in called_prompt
    assert "print('hello')" in called_prompt
