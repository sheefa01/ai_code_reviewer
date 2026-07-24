import typer
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.markdown import Markdown
from src.utils.file_parser import parse_python_files, check_syntax

from src.ai.reviewer import CodeReviewer
import os

app = typer.Typer(help="AI-Powered Python Code Reviewer")
console = Console()

@app.command()
def review(
    path: Path = typer.Argument(..., help="Path to a Python file or directory to review"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Path to save the markdown report")
):
    """
    Review Python files in the given path using Google Gemini.
    """
    console.print(f"[bold blue]Starting review for:[/bold blue] {path}")
    
    try:
        files = parse_python_files(path)
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(code=1)
        
    if not files:
        console.print("[yellow]No Python files found to review.[/yellow]")
        raise typer.Exit(code=0)
        
    console.print(f"Found [bold]{len(files)}[/bold] Python file(s). Checking syntax...")
    
    valid_files = []
    for file in files:
        is_valid, error = check_syntax(file)
        if not is_valid:
            console.print(f"[red]Syntax Error:[/red] {error}")
        else:
            valid_files.append(file)
            
    if not valid_files:
        console.print("[red]No valid Python files to review.[/red]")
        raise typer.Exit(code=1)

    console.print(f"[bold green]Syntax check complete.[/bold green] {len(valid_files)} file(s) ready for AI review.")
    
    try:
        reviewer = CodeReviewer()
    except ValueError as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {e}")
        console.print("Please copy [bold].env.example[/bold] to [bold].env[/bold] and add your GROQ API key.")
        raise typer.Exit(code=1)

    for file in valid_files:
        console.print(f"\n[bold magenta]--- Reviewing {file.name} ---[/bold magenta]")
        content = file.read_text(encoding="utf-8")
        
        with console.status(f"Generating review for {file.name}..."):
            feedback = reviewer.review_code(content, file.name)
            
        # Print beautifully using Rich Markdown
        console.print(Markdown(feedback))
        
        # Save to output file if flag is provided
        if output:
            try:
                # Append the review to the file
                with output.open("a", encoding="utf-8") as f:
                    f.write(f"\n\n# Review for {file.name}\n\n")
                    f.write(feedback)
            except Exception as e:
                console.print(f"[bold red]Failed to write to {output}:[/bold red] {e}")

    if output:
        console.print(f"\n[bold green]Report successfully saved to {output}[/bold green]")

if __name__ == "__main__":
    app()
