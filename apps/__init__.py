import sys
from typer import Typer
from apps import (
    modules
)

app = Typer()

app.add_typer(modules.modules_app, name="modules")

if __name__ == "__main__":
    sys.exit(1)