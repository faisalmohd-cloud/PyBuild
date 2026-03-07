import datetime
import shutil
import subprocess
from pathlib import Path

year: str = str(datetime.datetime.now().year)

mit_text: str = f"""MIT License

Copyright (c) {year} $$author-name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def choose_python() -> str:
    opts: list[str] = ["python", "python3", "py"]
    for opt in opts:
        if shutil.which(opt):
            return opt
    raise RuntimeError("Python is not installed or not in PATH")


def parse_pyb(path: Path) -> list[str]:
    text = path.read_text()

    lines = []
    for line in text.splitlines():
        line = line.split("#")[0].strip()
        if line and not line.startswith("#"):
            lines.append(line)

    name = None
    main = None
    icon = None
    window = "auto"
    onefile = True

    for line in lines:
        if line.startswith("executable("):
            name = line.split("(")[1].strip()

        elif line.startswith("main"):
            main = line.split(">>")[1].strip()

        elif line.startswith("icon"):
            icon = line.split(">>")[1].strip()

        elif line.startswith("window-type"):
            window = line.split(">>")[1].strip().lower()

        elif ".onedir" in line:
            onefile = False

    if not name or not main:
        raise RuntimeError("Invalid .pyb file")

    cmd = ["pyinstaller", "--name", name]

    if onefile:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")

    if icon and Path(icon).exists():
        cmd.extend(["--icon", icon])

    if window == "gui":
        cmd.append("--noconsole")
    elif window == "cli":
        cmd.append("--console")

    cmd.append(main)

    return cmd


def init_mit(path: Path) -> None:
    with open(path / "LICENSE", "w") as lic:
        lic.write(mit_text)


def init_core_project(project_name: str, project_path: Path, item_path: Path, git: bool, on_venv_start, on_venv_end,
                      on_git_start, on_git_end, on_git_not_found) -> None:
    project_path.mkdir(parents=True, exist_ok=True)
    item_path.mkdir(parents=True, exist_ok=True)

    on_venv_start()
    subprocess.run([choose_python(), "-m", "venv", ".venv"], cwd=project_path, check=True)
    on_venv_end()

    if git:
        if not shutil.which("git"):
            on_git_not_found()
        else:
            on_git_start()
            subprocess.run(["git", "init"], cwd=project_path, check=True)
            on_git_end()

    with open(project_path / "README.md", "w") as md:
        md.write(f"# {project_name}\n\n")

    with open(project_path / ".gitignore", "w") as gitignore:
        gitignore.write("""/build/
/dist/
/*.egg-info/
/.venv/
/__pycache__/
/.idea/
/.env/""")

    (project_path / "resources").mkdir(parents=True, exist_ok=True)


def init_executable(project_name: str, project_path: Path, item_name: str, item_path: Path, git: bool, on_venv_start,
                    on_venv_end, on_git_start, on_git_end, on_git_not_found, mit: bool) -> None:
    init_core_project(project_name, project_path, item_path, git, on_venv_start, on_venv_end, on_git_start, on_git_end,
                      on_git_not_found)

    with open(item_path / "main.py", "w") as py:
        py.write("""import sys

if __name__ == "__main__":
    print("Hello from PyBuild")
    sys.exit(0)
""")

    if mit:
        init_mit(project_path)

    with open(project_path / "PyExeBuild.pyb", "w") as pyb:
        pyb.write(f"""project({project_name} >> {project_path.resolve()}

executable({item_name}
    main >> {(item_path / "main.py").resolve()}
    icon >> {(project_path / "resources" / "icon.ico").resolve()}
    window-type >> AUTO
).onefile
""")


def init_library(project_name: str, project_path: Path, item_name: str, item_path: Path, git: bool, on_venv_start,
                 on_venv_end, on_git_start, on_git_end, on_git_not_found, mit: bool) -> None:
    init_core_project(project_name, project_path, item_path, git, on_venv_start, on_venv_end, on_git_start, on_git_end,
                      on_git_not_found)

    with open(item_path / f"{item_name}.py", "w") as py:
        py.write("""def get_greeting(name: str) -> str:
    return f"Hello {name}!"
""")

    with open(item_path / "__init__.py", "w") as py:
        py.write(f"""from . import {item_name}

__all__ = ["core"]
""")

    if mit:
        init_mit(project_path)

    license_line = 'license = "MIT"' if mit else ""

    with open(project_path / "pyproject.toml", "w") as toml:
        toml.write(f"""[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "{project_name}"
version = "0.1.0"
description = "A Python library"
readme = "README.md"
requires-python = ">=3.8"
authors = [
    {{ name = "author-name" }}
]
{license_line}
dependencies = []

[tool.setuptools.packages.find]
where = ["."]
""")


def build_executable(project_path: Path, clean: bool) -> None:
    if not shutil.which("pyinstaller"):
        raise RuntimeError("Pyinstaller is not installed. Run: pip install pyinstaller")

    if clean:
        for folder in ["build", "dist"]:
            p = project_path / folder
            if p.exists():
                shutil.rmtree(p)

    command: list[str] = parse_pyb(project_path / "PyExeBuild.pyb")
    command.insert(1, "--noconfirm")

    if clean:
        command.insert(2, "--clean")

    subprocess.run(command, check=True, cwd=project_path)


def build_library(project_path: Path, clean: bool) -> None:
    try:
        subprocess.run(
            [choose_python(), "-m", "build", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    except Exception:
        raise RuntimeError("Python module 'build' is not installed. Run: pip install build")

    if clean:
        build_dir = project_path / "build"
        dist_dir = project_path / "dist"

        if build_dir.exists():
            shutil.rmtree(build_dir)

        if dist_dir.exists():
            shutil.rmtree(dist_dir)

        for file in project_path.iterdir():
            if file.name.endswith(".egg-info"):
                shutil.rmtree(file)

    subprocess.run([choose_python(), "-m", "build"], check=True, cwd=project_path)