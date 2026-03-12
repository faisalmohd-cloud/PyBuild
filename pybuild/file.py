from pathlib import Path


class Ignore:
    def __init__(self):
        self.ignore_names = []

    def check(self, path: Path) -> bool:
        name = path.name
        if name in self.ignore_names:
            return True
        return False


def build_tree(root: Path, ignore: Ignore, max_lev: int = 3, lev: int = 0, prefix: str = "") -> str:
    if root is None:
        return "None"
    tree = [f"[bright_blue]{root.name}[/bright_blue]/"] if lev == 0 else []
    if lev >= max_lev:
        return "\n".join(tree)
    files = []
    try:
        for f in sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
            try:
                if not f.is_symlink() and not ignore.check(f):
                    files.append(f)
            except PermissionError:
                continue
    except PermissionError:
        pass
    last = len(files) - 1
    for i, file in enumerate(files):
        connector = "└── " if i == last else "├── "
        if file.is_file():
            tree.append(f"{prefix}{connector}{file.name}")
        else:
            tree.append(f"{prefix}{connector}[bright_blue]{file.name}[/bright_blue]/")
            new_prefix = prefix + ("    " if i == last else "│   ")
            subtree = build_tree(file, ignore, max_lev, lev + 1, new_prefix)
            if subtree:
                tree.append(subtree)
    return "\n".join(tree)
