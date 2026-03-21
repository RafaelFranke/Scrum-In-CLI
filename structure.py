from pathlib import Path


def load_in_order(path: Path, prefix: str) -> list[Path]:
    prefix += "-"
    dirs = []
    for dir in path.iterdir():
        if dir.is_dir() and dir.name.startswith(prefix):
            parts = dir.name.split("-")
            if len(parts) >= 1 and parts[1].isdigit():
                dirs.append((parts[1], dir, parts[2:] if len(parts) > 2 else []))
    dirs.sort(key=lambda x: x[0])
    return dirs


class Daily:
    DEFAULT_TEMPLATE_MD_JINJA = """
# Daily {{ date }} of Sprint {{ sprint_number }}

{% for member in members %}
## {{ member }}
What did you do until now?
- 

What will you do until next meeting?
- 

Do you have any impediments?
- 

{% endfor %}
    """

    def __init__(self, path: Path, number: int, date: str, sprint_number: int):
        self.path = path
        self.number = number
        self.date = date
        self.sprint_number = sprint_number

class Sprint:
    def __init__(self, path: Path):
        self.path = path
        self.dailies: list[Daily] = None

    def retro_path(self) -> Path:
        return self.path / "retro.json"
    
    def review_path(self) -> Path:
        return self.path / "review.json"
    
    def backlog_path(self) -> Path:
        return self.path / "backlog.json"
    
    def planning_path(self) -> Path:
        return self.path / "planning.json"
    
    def load_dailies(self) -> None:
        self.dailies = []
        daily_dirs = load_in_order(self.path, "daily")

        if daily_dirs[-1] and daily_dirs[-1][0] != len(daily_dirs):
            raise ValueError("Daily directories are not sequentially numbered")

        for _, path, _ in daily_dirs:
            self.dailies.append(Daily(path=path, number=int(path.name.split("-")[1]), date="", sprint_number=0))


class Structure:
    def __init__(self, toplevel_path: str):
        self.toplevel_path: Path = toplevel_path
        self.sprints: list[Sprint] = None

    def product_backlog_path(self) -> Path:
        return self.toplevel_path / "product_backlog.json"
    
    def definition_of_done_path(self) -> Path:
        return self.toplevel_path / "definition_of_done.json"

    def load_sprints(self) -> None:
        self.sprints = []
        sprint_dirs = load_in_order(self.toplevel_path, "sprint")

        if sprint_dirs[-1] and sprint_dirs[-1][0] != len(sprint_dirs):
            raise ValueError("Sprint directories are not sequentially numbered")

        for _, path, _ in sprint_dirs:
            self.sprints.append(Sprint(path=path))
    
    def create_next_sprint(self) -> Sprint:
        number = len(self.sprints) + 1
        sprint_dir = self.toplevel_path / f"sprint-{number:02d}"
        sprint_dir.mkdir()
        sprint = Sprint(path=sprint_dir)
        self.sprints.append(sprint)
        return sprint
    
    def fill_jinja_daily_template(self, template: str, ) -> str:
        from jinja2 import Template
        jinja_template = Template(template)
        return jinja_template.render(date=date, sprint_number=sprint_number, members=members)
