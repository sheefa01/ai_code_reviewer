import ast
from pathlib import Path
from typing import List, Tuple

def parse_python_files(path_str: str) -> List[Path]:
    """
    Given a file or directory path, returns a list of Python files.
    """
    path = Path(path_str)
    
    if not path.exists():
        raise FileNotFoundError(f"Path '{path_str}' does not exist.")
        
    if path.is_file():
        if path.suffix == '.py':
            return [path]
        return []
        
    if path.is_dir():
        return list(path.rglob("*.py"))
        
    return []

def check_syntax(file_path: Path) -> Tuple[bool, str]:
    """
    Checks if a Python file has valid syntax.
    Returns (True, "") if valid, (False, error_message) if invalid.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        ast.parse(content)
        return True, ""
    except SyntaxError as e:
        return False, f"Syntax error in {file_path}: {e}"
    except Exception as e:
        return False, f"Error reading {file_path}: {e}"
