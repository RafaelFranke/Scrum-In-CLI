from pathlib import Path

import typer

class Config:
    def __init__(self, project_name: str = None, members: list = None):
        self.project_name = project_name
        self.members = members

class State:
    def __init__(self, current_sprint: str = None, current_daily: str = None):
        self.current_sprint = current_sprint
        self.current_daily = current_daily

class Structure:
    class Daily:
        def __init__(self, name: str = None, path: Path = None):
            self.name: str = name
            self.path = path

    class Sprint:
        def __init__(self, name: str = None, path: Path = None):
            self.name: str = name
            self.path = path
            self.dailies = None
            self.retro = None
            self.review = None
            self.planning = None
            self.backlog = None

    def __init__(self, toplevel_path: str):
        self.toplevel_path: str = toplevel_path
        self.sprints: dict[str, Structure.Sprint] = None
        self.product_backlog = None
        self.definition_of_done = None

class Local:
    def __init__(self, editor: str = None):
        self.editor = editor


class Context:
    def from_path(path: str, fetch_config: bool = False, fetch_state: bool = False, fetch_structure: bool = False, fetch_local: bool = False) -> Context:
        pass

    def __init__(self, toplevel_path: str = None, fetch_config: bool = False, fetch_state: bool = False, fetch_structure: bool = False, fetch_local: bool = False):
        self.toplevel_path = toplevel_path
        self.config = Config() if fetch_config else None
        self.state = State() if fetch_state else None
        self.structure = Structure(toplevel_path) if fetch_structure else None
        self.local = Local() if fetch_local else None

def get_ctx(ctx: typer.Context, fetch_config: bool = False, fetch_state: bool = False, fetch_structure: bool = False, fetch_local: bool = False) -> Context:
    pass
