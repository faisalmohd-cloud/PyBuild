import zipfile
from pathlib import Path

if __name__ == "__main__":
    target_dir: Path = Path.cwd() / "dist" / "pybuild"
    output_file: Path = Path.cwd() / "dist" / "pybuild.zip"

    print(Path.cwd())
    print(target_dir)
    print(output_file)

    with zipfile.ZipFile(output_file, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in target_dir.rglob("*"):
            if file.is_file():
                archive_name = file.relative_to(target_dir)
                zf.write(file, archive_name)

    with open(output_file, "rb") as f:
        data = f.read()

    with open("pybuild_app_binary_code.py", "w") as f:
        f.write(f"APP_EXE_BIN: bytes = {repr(data)}\n")
