import pathlib


def print_folder_structure(root_dir, exclude=None, depth=0):
    exclude = exclude or []
    for path in pathlib.Path(root_dir).iterdir():
        if path.is_dir() and path.name not in exclude:
            print("|   " * depth + "|-- " + path.name)
            print_folder_structure(path, exclude, depth + 1)
        elif path.is_file() and path.suffix == ".py":
            print("|   " * depth + "|-- " + path.name)
        elif path.is_file() and path.suffix == ".toml":
            print("|   " * depth + "|-- " + path.name)


root_dir = r"/"
exclude = ["venv", "build", "dist", "golem_garden.egg-info", ".vscode", "golem_garden.egg-info", "__pycache__", ".git", ".idea", "github"]
print_folder_structure(root_dir, exclude)
