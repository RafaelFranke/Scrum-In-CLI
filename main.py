from pathlib import Path

import typer
from typing import Optional
from context import get_ctx
import json

app = typer.Typer(help="Scrum CLI")


### Globals 

CONFIG_0 = {
    "project_name": None,
    "members": [],
}

LOCAL_0 = {
    "editor": None,
}

STATE_0 = {
    "current_sprint": None,
    "current_daily": None,
}

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

    def write_json(file_path: Path, data: dict):
        with file_path.open("w") as f:
            json.dump(data, f, indent=4)
    
    write_json(scrum_dir / "config.json", CONFIG_0)
    write_json(scrum_dir / "state.json", STATE_0)
    write_json(scrum_dir / "local.json", LOCAL_0)


# Config

config_app = typer.Typer()
app.add_typer(config_app, name="config")

@config_app.command("set")
def config_set(key: str, value: str, ctx: typer.Context):
    context = get_ctx(ctx, fetch_config=True)
    typer.echo(f"set {key}={value}")

@config_app.command("get")
def config_get(key: str, ctx: typer.Context):
    context = get_ctx(ctx, fetch_config=True)
    typer.echo(f"get {key}")

@config_app.command("list")
def config_list(ctx: typer.Context):
    context = get_ctx(ctx, fetch_config=True)
    typer.echo("list config")

@config_app.command("unset")
def config_unset(key: str, ctx: typer.Context):
    context = get_ctx(ctx, fetch_config=True)
    typer.echo(f"unset {key}")


# Local config

local_app = typer.Typer()
app.add_typer(local_app, name="local")

@local_app.command("set")
def local_set(key: str, value: str, ctx: typer.Context):
    context = get_ctx(ctx, fetch_local=True)
    typer.echo(f"set {key}={value}")

@local_app.command("get")
def local_get(key: str, ctx: typer.Context):
    context = get_ctx(ctx, fetch_local=True)
    typer.echo(f"get {key}")

@local_app.command("list")
def local_list(ctx: typer.Context):
    context = get_ctx(ctx, fetch_local=True)
    typer.echo("list local config")

@local_app.command("unset")
def local_unset(key: str, ctx: typer.Context):
    context = get_ctx(ctx, fetch_local=True)
    typer.echo(f"unset {key}")

# statics 

@app.command("product-backlog")
def product_backlog(ctx: typer.Context):
    context = get_ctx(ctx, fetch_local=True)
    typer.echo("product backlog")

@app.command("definition-of-done")
def definition_of_done(ctx: typer.Context):
    context = get_ctx(ctx, fetch_local=True)
    typer.echo("definition of done")


# Sprint dependent commands

sprint_app = typer.Typer()
app.add_typer(sprint_app, name="sprint")


# Sprint

@sprint_app.command("next")
def sprint_next(name: str, ctx: typer.Context):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True)
    typer.echo(f"next sprint {name}")

@sprint_app.command("switch")
def sprint_switch(name: str, ctx: typer.Context):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True)
    typer.echo(f"switch sprint {name}")

@sprint_app.command("exit")
def sprint_exit(ctx: typer.Context):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True)
    typer.echo("exit sprint")

@sprint_app.command("list")
def sprint_list(ctx: typer.Context):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True)
    typer.echo("list sprints")

@sprint_app.command("show")
def sprint_show(ctx: typer.Context):
    context = get_ctx(ctx, fetch_state=True)
    typer.echo("show sprint")

@sprint_app.command("delete")
def sprint_delete(name: Optional[str] = None, ctx: typer.Context = None):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True)
    typer.echo(f"delete sprint {name}")


# Sprint documents

@sprint_app.command("planning")
def sprint_planning(ctx: typer.Context):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True, fetch_local=True)
    typer.echo("planning")

@sprint_app.command("backlog")
def sprint_backlog(ctx: typer.Context):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True, fetch_local=True)
    typer.echo("backlog")

@sprint_app.command("review")
def sprint_review(ctx: typer.Context):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True, fetch_local=True)
    typer.echo("review")

@sprint_app.command("retro")
def sprint_retro(ctx: typer.Context):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True, fetch_local=True)
    typer.echo("retro")


# Daily

daily_app = typer.Typer()
sprint_app.add_typer(daily_app, name="daily")


@daily_app.command("next")
def daily_next(name: str, ctx: typer.Context):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True)
    typer.echo(f"next daily {name}")

@daily_app.command("switch")
def daily_switch(name: str, ctx: typer.Context):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True)
    typer.echo(f"switch daily {name}")

@daily_app.command("exit")
def daily_exit(ctx: typer.Context):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True)
    typer.echo("exit daily")

@daily_app.command("list")
def daily_list(ctx: typer.Context):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True)
    typer.echo("list dailies")

@daily_app.command("show")
def daily_show(ctx: typer.Context):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True)
    typer.echo("show daily")

@daily_app.command("delete")
def daily_delete(ctx: typer.Context, name: Optional[str] = None):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True)
    typer.echo(f"delete daily {name}")

@daily_app.command("edit")
def daily_edit(ctx: typer.Context, raw: bool = typer.Option(False, "--raw")):
    context = get_ctx(ctx, fetch_state=True, fetch_structure=True, fetch_local=True, fetch_config=True)
    typer.echo(f"edit daily raw={raw}")

if __name__ == "__main__":
    app()