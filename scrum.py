from typing import Optional

import typer
from context import get_ctx, standard_edit
from main import app


@app.command("product-backlog")
def product_backlog(ctx: typer.Context):
    context = get_ctx(ctx, fetch_local=True, fetch_structure=True)
    editor = context.local.get_editor()
    if not editor:
        typer.echo("Error: No editor set in local config.")
        return
    standard_edit(editor, context.structure.product_backlog_path())

@app.command("definition-of-done")
def definition_of_done(ctx: typer.Context):
    context = get_ctx(ctx, fetch_local=True, fetch_structure=True)
    editor = context.local.get_editor()
    if not editor:
        typer.echo("Error: No editor set in local config.")
        return
    standard_edit(editor, context.structure.definition_of_done_path())


# Sprint dependent commands

sprint_app = typer.Typer()
app.add_typer(sprint_app, name="sprint")


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
app.add_typer(daily_app, name="daily")


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
