import pathlib
from pathlib import Path


class DirectoryWalker:
    """A class to walk through a directory and print its structure."""

    def __init__(self, root_dir: str):
        """
        Initialize the DirectoryWalker.

        Args:
            root_dir (str): The root directory to start walking from.
        """
        self.root_dir = Path(root_dir)

    def walk(self, current_dir: Path, indent_level: int = 0):
        """
        Recursively walk through a directory and print its structure.

        Args:
            current_dir (Path): The current directory to walk through.
            indent_level (int, optional): The indentation level for printing. Defaults to 0.
        """
        for item in current_dir.iterdir():
            print("  " * indent_level, item.name)
            if item.is_dir():
                if item.name in [".git", "__pycache__", "venv", ]:
                    continue
                print("  " * indent_level, "└──")
                self.walk(item, indent_level + 1)


    def print_structure(self):
        """
        Print the folder structure and files in the root directory.
        """
        self.walk(self.root_dir)


if __name__ == "__main__":
    # root_directory = input("Enter the root directory: ")
    root_directory = r"C:\Users\jonma\github_repos\jonmatthis\golem_garden"
    walker = DirectoryWalker(root_directory)
    walker.print_structure()
