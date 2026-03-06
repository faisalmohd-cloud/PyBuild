# PyBuild

**PyBuild** is a `lightweight`, `experimental` Python project initializer and builder that automates basic project setup.  
This app is currently in an experimental stage, so it’s best suited for `mini` projects.  
Future updates will expand support for multi-package initialization and more advanced builds.

> ⚠️ *Build support is minimal. It only works with a perfect `pyproject.toml` (for libraries) or `PyExeBuild.pyb` (for executables).*

---

## Usage

Installing and using PyBuild is simple:

1. Download the [installer from releases](https://www.github.com/bytesketch/PyBuild/releases/).  
2. Choose a path and install it.  
3. Use it via the terminal.

---

### Initialize a Project

```bash
pybuild init [path] [exe | lib] (--git)
```

#### Examples

Initialize an executable project in the current directory:

```bash
pybuild init . exe
```

Initialize a library project with Git in a `Projects` folder:

```bash
pybuild init Projects lib --git
```

---

## Platform Support

- **Windows:** Fully supported.  
- **Linux / macOS:** Currently **not supported**.

---

## Building PyBuild (Windows Only)

You can build the app and its installer in a few steps.

### Step 1: Clone the repository

```bash
git clone https://github.com/bytesketch/PyBuild.git
cd PyBuild
```

Or [download directly](https://github.com/bytesketch/PyBuild/archive/refs/heads/main.zip), unzip, and change into the directory.

---

### Step 2: Build the App

#### Option A: Using `make`

```bash
make
```

Yes, that’s all!  

#### Option B: Without `make` (Windows PowerShell)

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

## License

This project is licensed under **MIT 2026**.  
For full details, see [LICENSE](LICENSE).