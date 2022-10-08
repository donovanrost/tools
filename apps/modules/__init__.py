import sys

import typer
import inquirer
from apps.modules.AnsibleModuleInstaller.AnsibleModuleInstaller import AnsibleModuleInstaller

modules_app = typer.Typer()


@modules_app.command(name="list")
def list_roles():
    """
    Displays a list of all modules available for installation
    """
    installer = AnsibleModuleInstaller()
    modules = installer.get_modules()
    for module in modules:
        typer.secho(f"  {module['role']}", fg=typer.colors.MAGENTA)
        typer.secho(f"  {module['description']}")


@modules_app.command(name="install")
def install_role(name: str):
    """
    Installs the specified module
    """
    typer.echo(f"Installing {name}")
    installer = AnsibleModuleInstaller()
    installer.install_modules([name])


@modules_app.command(name="select")
def select_roles():
    installer = AnsibleModuleInstaller()
    modules = installer.get_modules()
    questions = [
        inquirer.Checkbox('modules',
                          message="What would you like to install?",
                          choices=modules,
                          )
    ]
    answers = inquirer.prompt(questions)['modules']

    if not answers:
        typer.echo("Nothing selected... exiting!")
        sys.exit(0)
    if answers:
        typer.echo(f"Installing {answers}")
        installer.install_modules(answers)


if __name__ == "__main__":
    sys.exit(1)
