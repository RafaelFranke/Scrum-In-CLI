from pathlib import Path
import json
import subprocess
import typer
from schema import Schema, And, Use, Optional, SchemaError
from structure import Structure


def standard_edit(editor: str, file_path: Path) -> None:
    if not file_path.exists():
        typer.echo(f"Creating file: {file_path}")
        file_path.touch()
    subprocess.run([editor, str(file_path)])

def assure_loaded(func) -> None:
    def wrapper(self: "JSONFile", *args, **kwargs):
        if self.__json is None:
            self.load()
        return func(self, *args, **kwargs)
    return wrapper

class JSONFile:
    SCHEMA: Schema = None
    DEFAULT: dict = None

    def __new__(cls, path: Path) -> "JSONFile":
        schema = getattr(cls, "SCHEMA", None)
        if schema is None:
            raise NotImplementedError(f"{cls.__name__} must define a SCHEMA class variable")
        return super().__new__(cls, path, schema)
    
    def __init__(self, path: Path, schema: Schema) -> None:
        self.path = path
        self.schema = schema
        self.__json = None

    def load(self) -> None:
        with self.path.open("r") as f:
            self.__json = json.load(f)
    
    @assure_loaded
    def validate(self) -> bool:
        try:
            self.schema.validate(self.__json)
            return True
        except SchemaError as e:
            typer.echo(f"Schema validation error: {e}")
            return False

    @assure_loaded
    def save(self) -> None:
        with self.path.open("w") as f:
            json.dump(self.__json, f, indent=4)

    def set(self, data: dict) -> None:
        self.__json = data

    @classmethod
    def from_default(cls, path: Path) -> "JSONFile":
        if getattr(cls, "DEFAULT", None) is None:
            raise ValueError(f"No DEFAULT defined for {cls.__name__}")
        inst = cls(path)
        inst.set(dict(cls.DEFAULT))
        inst.save()
        return inst


class Config(JSONFile):
    SCHEMA = Schema({
        "name": Optional(str),
        "members": Optional([str]),
    })

    DEFAULT = {
        "name": None,
        "members": [],
    }


class State(JSONFile):
    SCHEMA = Schema({
        "current_sprint": Optional(str),
        "current_daily": Optional(str),
    })

    DEFAULT = {
        "current_sprint": None,
        "current_daily": None,
    }

    @assure_loaded
    def set_current_sprint(self, sprint_name: str) -> None:
        self.__json["current_sprint"] = sprint_name
        self.save()

    @assure_loaded
    def set_current_daily(self, daily_name: str) -> None:
        self.__json["current_daily"] = daily_name
        self.save()


class Local(JSONFile):
    SCHEMA = Schema({
        "editor": Optional(str),
    })

    DEFAULT = {
        "editor": "nano",
    }

    def get_editor(self) -> str:
        return self.__json.get("editor", None)

    

class Context:
    def from_path(path: Path, fetch_config: bool = False, fetch_state: bool = False, fetch_structure: bool = False, fetch_local: bool = False) -> "Context":
        if not path.exists() or not path.is_dir():
            raise ValueError(f"Invalid path: {path}")
        while not (path / ".scrum").exists():
            if path.parent == path:
                raise ValueError("No .scrum directory found in path hierarchy")
            path = path.parent
        return Context(path, fetch_config, fetch_state, fetch_structure, fetch_local)

    def __init__(self, toplevel_path: Path = None, fetch_config: bool = False, fetch_state: bool = False, fetch_structure: bool = False, fetch_local: bool = False):
        self.toplevel_path = toplevel_path
        self.config = Config() if fetch_config else None
        self.state = State() if fetch_state else None
        self.structure = Structure(toplevel_path) if fetch_structure else None
        self.local = Local() if fetch_local else None

def get_ctx(ctx: typer.Context, fetch_config: bool = False, fetch_state: bool = False, fetch_structure: bool = False, fetch_local: bool = False) -> Context:
    path = Path("./").resolve()
    return Context.from_path(path, fetch_config, fetch_state, fetch_structure, fetch_local)
