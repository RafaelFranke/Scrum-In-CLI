import typer
from context import get_ctx
from main import app


config_app = typer.Typer()
app.add_typer(config_app, name="config")
config_app_set = typer.Typer()
config_app.add_typer(config_app_set, name="set")
config_app_get = typer.Typer()
config_app.add_typer(config_app_get, name="get")

@config_app_set.command("name")
def config_set_name(value: str, ctx: typer.Context):
    context = get_ctx(ctx, fetch_config=True)
    context.config.__json["name"] = value
    context.config.save()

@config_app_get.command("name")
def config_get_name(ctx: typer.Context):
    context = get_ctx(ctx, fetch_config=True)
    name = context.config.__json.get("name")
    typer.echo(f"name: {name if name else 'not set'}")

@config_app_set.command("members")
def config_set_members(*value: str, ctx: typer.Context):
    context = get_ctx(ctx, fetch_config=True)
    members = [member.strip() for member in value]
    context.config.__json["members"] = members
    context.config.save()

@config_app_get.command("members")
def config_get_members(ctx: typer.Context):
    context = get_ctx(ctx, fetch_config=True)
    members = context.config.__json.get("members", [])
    typer.echo("members:")
    if members:
        for member in members:
            typer.echo(f"- {member}")
    else:
        typer.echo("not set")


# Local config

local_app = typer.Typer()
app.add_typer(local_app, name="local")
local_app_set = typer.Typer()
local_app.add_typer(local_app_set, name="set")
local_app_get = typer.Typer()
local_app.add_typer(local_app_get, name="get")

@local_app_set.command("editor")
def local_set_editor(value: str, ctx: typer.Context):
    context = get_ctx(ctx, fetch_local=True)
    context.local.__json["editor"] = value
    context.local.save()

@local_app_get.command("editor")
def local_get_editor(ctx: typer.Context):
    context = get_ctx(ctx, fetch_local=True)
    editor = context.local.__json.get("editor")
    typer.echo(f"editor: {editor if editor else 'not set'}")
