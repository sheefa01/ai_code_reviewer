import pytest
from pathlib import Path
from src.utils.file_parser import parse_python_files, check_syntax

def test_parse_python_files_with_file(tmp_path: Path):
    test_file = tmp_path / "test.py"
    test_file.write_text("print('hello')")
    
    files = parse_python_files(str(test_file))
    assert len(files) == 1
    assert files[0] == test_file

def test_parse_python_files_with_directory(tmp_path: Path):
    (tmp_path / "test1.py").write_text("print('hello')")
    (tmp_path / "test2.py").write_text("print('world')")
    (tmp_path / "not_python.txt").write_text("hello")
    
    files = parse_python_files(str(tmp_path))
    assert len(files) == 2

def test_check_syntax_valid(tmp_path: Path):
    test_file = tmp_path / "valid.py"
    test_file.write_text("def my_func():\n    return True\n")
    
    is_valid, error = check_syntax(test_file)
    assert is_valid is True
    assert error == ""

def test_check_syntax_invalid(tmp_path: Path):
    test_file = tmp_path / "invalid.py"
    test_file.write_text("def my_func()  # missing colon and invalid syntax\n    return True\n")
    
    is_valid, error = check_syntax(test_file)
    assert is_valid is False
    assert "Syntax error" in error
