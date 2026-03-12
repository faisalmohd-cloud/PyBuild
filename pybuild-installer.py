import os
import shutil
import sys
import winreg
import zipfile
from pathlib import Path

from rich import print

from pybuild_app_binary_code import APP_EXE_BIN

if __name__ == "__main__":
    print("[bright_blue]Setting up environment...[/bright_blue]")

    zip_path: Path = Path(os.getenv("PROGRAMDATA")) / "tmp"
    zip_path.mkdir(parents=True, exist_ok=True)
    zip_path /= "pybuild-installer.zip"

    with open(zip_path, "wb") as f:
        f.write(APP_EXE_BIN)

    print("Installing Pybuild...")

    if not shutil.which("pybuild"):
        install_path: Path = Path(
            input("> Enter full path to install: ").strip() or os.path.join(os.getenv("LOCALAPPDATA"), "PyBuild"))
        print(f"Installing at: [bright_blue]{install_path.resolve()}[/bright_blue]")
        confirm: bool = input("Install? [Y/n]: ").lower().strip() != "n"

        if not confirm:
            print("[bright_yellow]Aborting install...[/bright_yellow]")
            input("Press enter to continue...")
            sys.exit()

        install_path.mkdir(parents=True, exist_ok=True)
    else:
        install_path: Path = Path(shutil.which("pybuild")).parent
        confirm: bool = input("PyBuild already installed...\nUpdate? [Y/n]: ").lower().strip() != "n"

        if not confirm:
            print("[bright_yellow]Aborting update...[/bright_yellow]")
            input("Press enter to continue...")
            sys.exit()

    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(install_path)

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
            try:
                path_value, regtype = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                path_value = ""
                regtype = winreg.REG_EXPAND_SZ

            install_str = str(install_path)
            paths = path_value.split(";") if path_value else []

            if install_str not in paths:
                new_path = path_value + (";" if path_value else "") + install_str
                winreg.SetValueEx(key, "Path", 0, regtype, new_path)
                print("[bright_green]Added install directory to PATH.[/bright_green]")
            else:
                pass

        print("[bright_green]Installation successful![/bright_green]")

    except KeyboardInterrupt:
        print("[bright_yellow]Aborting installation...[/bright_yellow]")

        if install_path.exists():
            shutil.rmtree(install_path)
            print("[bright_green]System restored to previous state.[/bright_green]")

    except Exception as e:
        print(f"[bright_yellow]Error:[/bright_yellow] [bright_red]{e}[/bright_red]")

        if install_path.exists():
            shutil.rmtree(install_path)
            print("[bright_green]System restored to previous state.[/bright_green]")

    zip_path.unlink()
    input("Press enter to continue...")
