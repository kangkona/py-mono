"""CLI entry point for py-coding-agent."""

import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from py_ai import LLM
from .agent import CodingAgent

app = typer.Typer(
    name="py-code",
    help="Interactive coding agent CLI",
    add_completion=False,
)
console = Console()


@app.command()
def main(
    model: Optional[str] = typer.Option(None, "--model", "-m", help="LLM model to use"),
    provider: str = typer.Option("openai", "--provider", "-p", help="LLM provider"),
    workspace: Path = typer.Option(".", "--path", "-w", help="Workspace directory"),
    verbose: bool = typer.Option(True, "--verbose/--quiet", "-v/-q", help="Verbose output"),
    resume: bool = typer.Option(False, "--resume", "-r", help="Resume last session"),
    continue_session: bool = typer.Option(False, "--continue", "-c", help="Continue last session"),
    session_name: Optional[str] = typer.Option(None, "--session", "-s", help="Session name"),
    no_extensions: bool = typer.Option(False, "--no-extensions", help="Disable extensions"),
    no_skills: bool = typer.Option(False, "--no-skills", help="Disable skills"),
):
    """Start interactive coding agent."""
    # Get API key
    api_key = os.getenv(f"{provider.upper()}_API_KEY")
    if not api_key:
        console.print(f"[red]Error: {provider.upper()}_API_KEY not set[/red]")
        console.print(f"Please set your API key: export {provider.upper()}_API_KEY=your-key")
        raise typer.Exit(1)

    # Create LLM
    llm = LLM(
        provider=provider,
        api_key=api_key,
        model=model or ("gpt-3.5-turbo" if provider == "openai" else None),
    )

    # Handle session loading
    session_path = None
    if resume or continue_session:
        from py_agent_core import SessionManager
        
        session_mgr = SessionManager(workspace)
        sessions = session_mgr.list_sessions(limit=10)
        
        if not sessions:
            console.print("[yellow]No previous sessions found[/yellow]")
        elif continue_session or len(sessions) == 1:
            # Auto-continue most recent
            session_path = sessions[0].path
            console.print(f"[cyan]Continuing:[/cyan] {sessions[0].session_name}")
        else:
            # Show selection UI
            console.print("[cyan]Recent sessions:[/cyan]\n")
            console.print(session_mgr.format_session_list(sessions))
            console.print()
            
            from py_tui import Prompt
            prompt = Prompt()
            
            try:
                choice = prompt.ask(
                    "Select session (number or name)",
                    default="1"
                )
                
                # Parse choice
                if choice.isdigit() and 1 <= int(choice) <= len(sessions):
                    session_path = sessions[int(choice) - 1].path
                else:
                    # Try by name
                    found = session_mgr.find_session(choice)
                    if found:
                        session_path = found
                    else:
                        console.print(f"[yellow]Session '{choice}' not found, starting new[/yellow]")
            except (KeyboardInterrupt, EOFError):
                console.print("[yellow]Starting new session[/yellow]")

    # Create and run agent
    agent = CodingAgent(
        llm=llm,
        workspace=str(workspace),
        verbose=verbose,
        session_name=session_name,
        session_path=session_path,
        enable_extensions=not no_extensions,
        enable_skills=not no_skills,
    )

    console.print(f"[green]✓ Coding Agent started[/green]")
    console.print(f"Model: [cyan]{llm.config.model}[/cyan]")
    console.print(f"Workspace: [cyan]{workspace.resolve()}[/cyan]")
    
    if agent.session:
        console.print(f"Session: [cyan]{agent.session.name}[/cyan]")
    
    if agent.skill_manager and len(agent.skill_manager) > 0:
        console.print(f"Skills: [cyan]{len(agent.skill_manager)} loaded[/cyan]")
    
    if agent.extension_manager and len(agent.extension_manager.extensions) > 0:
        console.print(f"Extensions: [cyan]{len(agent.extension_manager.extensions)} loaded[/cyan]")
    
    console.print()
    console.print("[dim]Type /help for commands, /exit to quit[/dim]")
    console.print()

    agent.run_interactive()


@app.command()
def gen(
    description: str = typer.Argument(..., help="What to generate"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="LLM model"),
):
    """Generate code from description."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[red]Error: OPENAI_API_KEY not set[/red]")
        raise typer.Exit(1)

    llm = LLM(api_key=api_key, model=model or "gpt-3.5-turbo")
    agent = CodingAgent(llm=llm, verbose=False)

    console.print(f"[cyan]Generating:[/cyan] {description}")
    result = agent.run_once(f"Generate code for: {description}")

    if output:
        output.write_text(result)
        console.print(f"[green]Saved to:[/green] {output}")
    else:
        console.print(result)


@app.command()
def analyze(
    path: Path = typer.Argument(..., help="File or directory to analyze"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="LLM model"),
):
    """Analyze code and provide insights."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        console.print("[red]Error: OPENAI_API_KEY not set[/red]")
        raise typer.Exit(1)

    if not path.exists():
        console.print(f"[red]Error: {path} does not exist[/red]")
        raise typer.Exit(1)

    llm = LLM(api_key=api_key, model=model or "gpt-3.5-turbo")
    agent = CodingAgent(llm=llm, verbose=False)

    console.print(f"[cyan]Analyzing:[/cyan] {path}")
    result = agent.run_once(f"Analyze the file {path} and provide insights")
    console.print(result)


if __name__ == "__main__":
    app()
