"""Main CLI entry point for Ask PanDA."""


import typer
from rich.console import Console

app = typer.Typer(
    name="ask-panda",
    help="A flexible API for building smart assistants for PanDA workflows",
)
console = Console()


@app.command()
def query(
    question: str = typer.Argument(..., help="The question to ask"),
    experiment: str = typer.Option("atlas", "--experiment", "-e", help="Experiment to query"),
    client: str | None = typer.Option(None, "--client", "-c", help="Specific client to use"),
) -> None:
    """Ask a question about PanDA workflows."""
    console.print(f"[bold blue]Query:[/bold blue] {question}")
    console.print(f"[bold green]Experiment:[/bold green] {experiment}")
    if client:
        console.print(f"[bold yellow]Client:[/bold yellow] {client}")

    # Placeholder response
    console.print("\n[bold]Response:[/bold]")
    console.print(f"Processing query for {experiment} experiment...")


@app.command()
def chat(
    experiment: str = typer.Option("atlas", "--experiment", "-e", help="Experiment to chat with"),
) -> None:
    """Start an interactive chat session."""
    console.print(f"[bold blue]Starting chat session for {experiment} experiment...[/bold blue]")
    console.print("Type 'quit' or 'exit' to end the session.\n")

    while True:
        try:
            user_input = typer.prompt("You")
            if user_input.lower() in ("quit", "exit"):
                console.print("[bold]Goodbye![/bold]")
                break
            console.print(f"[bold green]Assistant:[/bold green] I understand you're asking about: {user_input}")
        except KeyboardInterrupt:
            console.print("\n[bold]Session ended.[/bold]")
            break


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind to"),
    experiment: str = typer.Option("atlas", "--experiment", "-e", help="Default experiment"),
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug mode"),
) -> None:
    """Start the API server."""
    import uvicorn

    from ask_panda.api.app import create_app
    from ask_panda.config.schemas import ServerConfig

    console.print("[bold blue]Starting Ask PanDA API server...[/bold blue]")
    console.print(f"Host: {host}")
    console.print(f"Port: {port}")
    console.print(f"Default experiment: {experiment}")
    console.print(f"Debug mode: {debug}")

    config = ServerConfig(host=host, port=port, debug=debug)
    api_app = create_app(config)

    uvicorn.run(api_app, host=host, port=port)


@app.command()
def list_experiments() -> None:
    """List available experiments."""
    experiments = [
        ("atlas", "ATLAS experiment at CERN LHC"),
        ("verarubin", "Vera C. Rubin Observatory LSST"),
        ("epic", "ePIC detector at the Electron-Ion Collider"),
    ]

    console.print("[bold blue]Available experiments:[/bold blue]\n")
    for name, description in experiments:
        console.print(f"  [bold]{name}[/bold]: {description}")


@app.command()
def version() -> None:
    """Show version information."""
    from ask_panda import __version__

    console.print(f"[bold]Ask PanDA API[/bold] version {__version__}")


if __name__ == "__main__":
    app()
