# tool.py
import time
import click
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

@click.group()
def cli():
    """My daily utility CLI."""
    pass

@cli.command()
@click.option("--count", default=5, help="Number of items to process")
def process(count):
    """Process N items with a progress bar."""
    console.print("[bold cyan]Starting process...[/bold cyan]")
    results = []
    for i in track(range(count), description="Processing"):
        time.sleep(0.2)  # simulate work
        results.append({"item": i, "status": "ok"})
    
    table = Table(title="Results")
    table.add_column("Item", style="cyan")
    table.add_column("Status", style="green")
    for r in results:
        table.add_row(str(r["item"]), r["status"])
    console.print(table)

@cli.command()
def status():
    """Quick status check."""
    console.print("[bold green]✓ Everything is fine[/bold green]")

if __name__ == "__main__":
    cli()