import typer
from rich.console import Console
from src.utils.file_parser import parse_python_files, check_syntax

app = typer.Typer(help="AI-Powered Python Code Reviewer")
console = Console()

@app.command()
def review(path: str = typer.Argument(..., help="Path to a Python file or directory to review")):
    """
    Review Python files in the given path.
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
            
    console.print(f"[bold green]Syntax check complete.[/bold green] {len(valid_files)} file(s) ready for AI review.")
    
    # Placeholder for Milestone 3 AI integration
    if valid_files:
        console.print("\n[dim]AI review logic will be implemented in Milestone 3...[/dim]")

if __name__ == "__main__":
    app()
