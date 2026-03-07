import os
import subprocess
import sys
import time
from pathlib import Path

import typer
from rich import print
from rich.console import Console
from rich.table import Table

import core
from project_type import ProjectType

app: typer.Typer = typer.Typer()
console: Console = Console()

VERSION: str = "1.0-rc2.windows"


@app.callback()
def main() -> None:
    pass


def venv_start() -> None:
    print("[bright_blue]Initializing Virtual Environment...[/bright_blue]")


def venv_end() -> None:
    print("[bright_green]Virtual Environment Initialized.[/bright_green]")


def git_start() -> None:
    print("[bright_blue]Initializing Empty Git Repository...[/bright_blue]")


def git_end() -> None:
    print("[bright_green]Git Repository Initialized.[/bright_green]")


def git_not_found() -> None:
    print("[bright_yellow]Git is not installed.[/bright_yellow]")
    print("[bright_blue]Aborting Git Initialization.[/bright_blue]")


# noinspection PyShadowingBuiltins
@app.command()
def help() -> None:
    console.print("[bold bright_cyan]PyBuild CLI Help[/bold bright_cyan]\n")
    console.print("PyBuild is a project build tool for Python libraries and executables.\n")

    console.print("[bold]Usage:[/bold]")
    console.print("  [bright_white]pybuild[/bright_white] [bright_cyan]<command>[/bright_cyan] "
                  "[bright_yellow]<path>[/bright_yellow] [bright_blue]<exe|lib>[/bright_blue] "
                  "[dim][--git][/dim]\n")

    console.print("[bold]Commands:[/bold]")
    table = Table(show_header=True, header_style="bold bright_white", show_lines=True)
    table.add_column("Command", style="bright_cyan", width=12)
    table.add_column("Description", style="white")
    table.add_column("Options / Notes", style="bright_yellow")

    table.add_row("init", "Initialize a new project (library or executable).",
                  "[bold]--git[/bold]: initialize a Git repository")
    table.add_row("build", "Build an existing project.", "[bold]--clean[/bold]: clean build before building")
    table.add_row("version", "Show PyBuild version.", "")
    table.add_row("help", "Show this help message.", "")

    console.print(table)

    console.print("\n[bold]Interactive Mode:[/bold]")
    console.print("  Run [bright_white]pybuild[/bright_white] with no arguments to start the interactive shell mode.\n")
    console.print("[bold]Examples:[/bold]")
    console.print("  pybuild init . exe --git")
    console.print("  pybuild build Project --clean\n")

    console.print("[bold]Notes:[/bold]")
    console.print("  - Library projects require a 'pyproject.toml'.")
    console.print("  - Executable projects require a 'PyExeBuild.pyb'.")
    console.print("[dim]For more detailed documentation, refer to README or PyBuild docs.[/dim]")


@app.command()
def init(path: str, project_type: ProjectType,
         git: bool = typer.Option(False, "--git", help="Initialize a git repository")) -> None:
    project_name: str = typer.prompt("Enter project name")
    project_path: Path = Path(path) / project_name

    if project_path.exists() and project_path.is_dir() and len(os.listdir(str(project_path))) > 0:
        raise typer.BadParameter(f"Directory {project_path.resolve()} already exists")

    item_name: str = typer.prompt(f"Enter {'library' if project_type == ProjectType.LIBRARY else 'executable'} name")
    item_path: Path = Path(project_path) / item_name

    mit_init: bool = typer.confirm("Initialize MIT License?", default=False)

    try:
        if project_type == ProjectType.LIBRARY:
            core.init_library(project_name, project_path, item_name, item_path, git, venv_start, venv_end, git_start,
                              git_end, git_not_found, mit_init)
        else:
            core.init_executable(project_name, project_path, item_name, item_path, git, venv_start, venv_end, git_start,
                                 git_end, git_not_found, mit_init)
        print(f"[bright_green]Successfully initialized project:[/bright_green] [dim]{project_name}[/dim]")
    except Exception as e:
        print(f"[bright_red]Error:[/bright_red] Cannot initialize project: [dim]{e}[/dim]")


@app.command()
def build(path: str, clean: bool = typer.Option(False, help="Build clean library or executable.")) -> None:
    project_path: Path = Path(path)

    if not project_path.exists() or not project_path.is_dir():
        raise typer.BadParameter(f"Directory {project_path.resolve()} does not exist or is not a directory")

    if len(os.listdir(str(project_path))) == 0:
        raise typer.BadParameter(f"Directory {project_path.resolve()} does not contain any files")

    project_type: ProjectType | None = None

    for file in project_path.iterdir():
        if file.is_file() and file.name == "PyExeBuild.pyb":
            project_type = ProjectType.EXECUTABLE
            break

        if file.is_file() and file.name == "pyproject.toml":
            project_type = ProjectType.LIBRARY
            break

    if project_type is None:
        raise typer.BadParameter(
            f"Directory {project_path.resolve()} does not contain any build file configured by PyBuild.")

    try:
        start: float = time.time()
        if project_type == ProjectType.LIBRARY:
            core.build_library(project_path, clean)
        else:
            core.build_executable(project_path, clean)
        print(
            f"[bright_green]Successfully built project:[/bright_green] in [dim]{round(time.time() - start, 2)} seconds.[/dim]")
    except Exception as e:
        print(f"[bright_red]Error:[/bright_red] Cannot build project: [dim]{e}[/dim]")


@app.command()
def version() -> None:
    print(f"[dim]PyBuild version:[/dim] [bright_cyan]{VERSION}[/bright_cyan]")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("[bright_cyan]Welcome to PyBuild![/bright_cyan]")
        print("Now type commands without 'pybuild'")
        print("Use [bright_blue]exit[/bright_blue] to exit")

        while True:
            cmd = ["pybuild"]
            cmd.extend(input(">> ").strip().split())
            if cmd[1] == "exit":
                break
            subprocess.run(cmd, check=True)
        print("[bright_yellow]Exiting...[/bright_yellow]")
    else:
        cmd = sys.argv[1].lower()
        if cmd.startswith("--"):
            print("[bright_red]Error:[/bright_red] This app do not support option with '--'")
        else:
            app()
