import os
import pytest
from unittest.mock import patch, MagicMock
from src.ai.reviewer import CodeReviewer

@patch.dict(os.environ, {"GROQ_API_KEY": "test_key"})
@patch("src.ai.reviewer.Groq")
def test_reviewer_initialization_success(mock_groq):
    reviewer = CodeReviewer()
    mock_groq.assert_called_once_with(api_key="test_key")
    assert reviewer.model_name == 'llama-3.1-8b-instant'

@patch.dict(os.environ, {}, clear=True)
def test_reviewer_initialization_failure():
    with pytest.raises(ValueError, match="GROQ_API_KEY is missing"):
        CodeReviewer()

@patch.dict(os.environ, {"GROQ_API_KEY": "test_key"})
@patch("src.ai.reviewer.Groq")
def test_review_code_success(mock_groq):
    # Setup mock
    mock_client_instance = MagicMock()
    mock_groq.return_value = mock_client_instance
    mock_choice = MagicMock()
    mock_choice.message.content = "This is a great test review."
    mock_client_instance.chat.completions.create.return_value.choices = [mock_choice]
    
    reviewer = CodeReviewer()
    feedback = reviewer.review_code("print('hello')", "test.py")
    
    assert feedback == "This is a great test review."
    mock_client_instance.chat.completions.create.assert_called_once()
    
    # Check if the prompt contains our code and filename
    called_messages = mock_client_instance.chat.completions.create.call_args[1]['messages']
    called_prompt = called_messages[0]['content']
    assert "test.py" in called_prompt
    assert "print('hello')" in called_prompt
