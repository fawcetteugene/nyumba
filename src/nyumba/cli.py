import typer
from rich import print as rprint
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from typing import List
from .models import AgreementInput
from .orchestrator import orchestrate
from .agents.witness import run as witness_run
from .agents.receipt import generate_receipt
import uvicorn

app = typer.Typer()

@app.command()
def add(text: str, location: str, participants: str):
    """Add a new agreement."""
    parts = [p.strip() for p in participants.split(",")]
    inp = AgreementInput(text=text, location=location, participants=parts)
    with Live(auto_refresh=False, vertical_overflow="visible") as live:
        table = Table(title="Nyumba Agent Events")
        table.add_column("Agent", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Message")
        for event in orchestrate(inp):
            table.add_row(event.agent, event.status, event.message)
            live.update(Panel(table, title="Live Events"), refresh=True)
    rprint("[bold green]Agreement added successfully![/]")

@app.command()
def witness(agreement_id: str, yes: bool = True, note: str = ""):
    """Vote as a witness."""
    result = witness_run(agreement_id, yes, note)
    rprint(f"[bold]Vote recorded.[/] Total yes votes: {result.get('total_yes_votes', 0)}")
    if result.get("verified_now"):
        rprint("[bold green]Agreement is now community verified![/]")

@app.command()
def receipt(agreement_id: str):
    """Generate a peace receipt."""
    result = generate_receipt(agreement_id)
    if "error" in result:
        rprint(f"[red]{result['error']}[/]")
    else:
        rprint(f"[green]Receipt generated:[/] {result['qr_path']}")
        rprint(f"[yellow]SMS text:[/] {result['sms_text']}")

@app.command()
def serve(port: int = 8765):
    """Run the FastAPI server."""
    rprint(f"[bold blue]Starting Nyumba server on http://localhost:{port}[/]")
    uvicorn.run("src.nyumba.server:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    app()
