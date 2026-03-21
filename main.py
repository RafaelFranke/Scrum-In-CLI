from pathlib import Path

import typer
from typing import Optional
from context import get_ctx, Config, State, Local

app = typer.Typer(help="Scrum CLI")

import settings  # noqa: F401
import scrum  # noqa: F401


### Globals

@app.command()
def init(
    path: Path = typer.Option(
        Path("./"),
        "--path",
        "-p",
        help="Target directory where .scrum will be created",
        exists=False,
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
    ),
    force: bool = typer.Option(False, "--force", help="Overwrite existing .scrum directory"),
):
    scrum_dir = path / ".scrum"
    if scrum_dir.exists():
        if not force:
            typer.echo(f"Error: {scrum_dir} already exists. Use --force to overwrite.")
            raise typer.Exit(code=1)
        else:
            typer.echo(f"Warning: {scrum_dir} already exists. Overwriting due to --force.")

    scrum_dir.mkdir(parents=True, exist_ok=True)
    
    Config.from_default(scrum_dir / "config.json")
    State.from_default(scrum_dir / "state.json")
    Local.from_default(scrum_dir / "local.json")


if __name__ == "__main__":
    app()