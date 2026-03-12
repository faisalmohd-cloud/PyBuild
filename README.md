# PyBuild

**PyBuild** is a `lightweight`, `experimental` Python project initializer and builder.  
It automates project setup and basic build tasks for Python **libraries** and **executables**.

> ⚠️ *Experimental: Best suited for small projects. Build support requires either a `pyproject.toml` (library) or `PyExeBuild.pyb` (executable).*

---

## Features

- Initialize **Python libraries** or **executables** with recommended structure
- Optional **Git repository** initialization
- Virtual environment setup automatically
- Build libraries (`build`) and executables (`pyinstaller`)
- Clean builds with `--clean` option
- Interactive shell for quick file operations (`ls`, `cd`, `mkdir`, etc.)

---

## Installation

1. Download the [latest release](https://github.com/bytesketch/PyBuild/releases/)
2. Install by running the downloaded `.exe` (Windows only)
3. Use PyBuild from terminal:

```bash
pybuild <command> [path] [exe|lib] [--git | --clean]
```

> Windows only. Linux/macOS support coming in future updates.

---

## CLI Usage

### Initialize a Project

```bash
pybuild init <path> <exe|lib> [--git]
```

**Examples:**

- Executable in current directory:

```bash
pybuild init . exe
```

- Library in `Projects` folder with Git:

```bash
pybuild init Projects lib --git
```

> You will be prompted for project and item names. Optionally, you can initialize an MIT License.

---

### Build a Project

```bash
pybuild build <path> [--clean]
```

- `--clean` removes previous `build` and `dist` directories and cleans library artifacts.
- PyBuild detects project type automatically (`PyExeBuild.pyb` → executable, `pyproject.toml` → library).

**Examples:**

```bash
pybuild build MyLibrary --clean
pybuild build MyExe
```

---

### Other Commands

- `pybuild help` – Show CLI help  
- `pybuild version` – Show PyBuild version

---

### Interactive Mode

Run PyBuild without arguments:

```bash
pybuild
```

You get an interactive shell with:

- `ls [path] [ignore=[name1|name2]] [max=N]` – Directory tree
- `cd <path>` – Change directory
- `mkdir <name>` – Create folder
- `rm <file|folder>` – Remove file/folder
- `touch <file>` – Create file
- `cp <src> <dst>` – Copy file/folder
- `mv <src> <dst>` – Move file/folder
- `exit` – Exit shell

---

## Building PyBuild (Windows Only)

You can build PyBuild from source using **Makefile** or PowerShell scripts.

### Using `make` (Recommended)

```bash
make
```

- Builds app → binary → installer in sequence
- Output installer: `dist/PyBuild-Installer.exe`

**Other targets:**

- `make clean` – Remove build artifacts
- `make install_clean` – Clean + run installer

---

### Without `make` (Manual)

1. Build the app:

   ```powershell
   powershell -ExecutionPolicy Bypass -File pybuild.build.ps1
   ```

2. Build the binary:

   ```bash
   python binary-build.py
   ```

3. Build the installer:

   ```powershell
   powershell -ExecutionPolicy Bypass -File installer.build.ps1
   ```

---

## Roadmap

- [x] Prototype core functionality
- [x] Executable project support
- [x] Installer creation
- [x] Stable Windows release
- [ ] Templates for libraries and executables
- [ ] Improved CLI output and help system
- [ ] MIT license automation
- [ ] Cross-platform support (Linux/macOS)
- [ ] Publish on PyPI (`pip install pybuild`)
- [ ] Interactive shell improvements (color-coded output, advanced commands)
- [ ] Multi-package/multi-module project support
- [ ] GUI builder for beginners
- [ ] Finalization

---

## Project Structure

**Executable (`exe`) Example:**

```text
ProjectName/
├─ .git/...         # If '--git'
├─ .venv/...
├─ resources/
├─ PyExeBuild.pyb
├─ main/
│   └─ main.py
├─ README.md
├─ LICENSE
└─ .gitignore
```

**Library (`lib`) Example:**

```text
ProjectName/
├─ .git/...         # If '--git'
├─ .venv/...
├─ item_name/
│   ├─ __init__.py
│   └─ item_name.py
├─ pyproject.toml
├─ README.md
├─ LICENSE
└─ .gitignore
```

---

## Version

- **1.0-windows** – Stable release  
- **1.0-rc2.windows** – Added `collect-all` support, cleaner output, safer comment parsing  
- **1.0-rc1.windows** – Experimental

---

## License

**MIT License 2026**  
See [LICENSE](LICENSE) for full details.

