import pathlib
from datetime import datetime
from pathlib import Path


class DirectoryWalker:
    """A class to walk through a directory and print its structure."""

    def __init__(self,
                 root_dir: str,
                 excluded_directories: list = [],
                 included_file_extensions: list = [], ):
        """
        Initialize the DirectoryWalker.

        Args:
            root_dir (str): The root directory to start walking from.
        """
        self.root_dir = Path(root_dir)
        self._excluded_directories = excluded_directories
        self._included_file_extensions = included_file_extensions
        self._excluded_files = [".DS_Store"]
        self._excluded_file_extensions = [".pyc"]

    def walk(self, current_dir: Path, indent_level: int = 0):
        """
        Recursively walk through a directory and print its structure.

        Args:
            current_dir (Path): The current directory to walk through.
            indent_level (int, optional): The indentation level for printing. Defaults to 0.
        """
        output_text = ""
        for item in current_dir.iterdir():
            if item.is_file():
                if item.name in self._excluded_files:
                    continue
                if item.suffix in self._excluded_file_extensions:
                    continue
                if item.name in self._included_file_extensions:
                    output_text += "│   " * indent_level + "├── " + item.name +   "\n"
                else:
                    output_text += "│   " * indent_level + "├── " + item.name +   "\n"
            if item.is_dir():
                if item.name in self._excluded_directories:
                    continue
                output_text += "│   " * indent_level + "└── " + item.name +   "/\n"
                output_text += self.walk(item, indent_level + 1)

        return output_text

    def print_structure(self):
        """
        Print the folder structure and files in the root directory.
        """
        output_text = self.walk(self.root_dir)
        print(self.root_dir.name + "/  ")
        print(output_text)
        self._save_to_markdown_file(output_text)

    def _save_to_markdown_file(self, output_text):
        now = self._get_current_timestamp()
        md_path = Path(__file__).parent / "output" / f"copy_of_directories_on_{now}_output.md"
        md_path.parent.mkdir(parents=True, exist_ok=True)
        output_text = self._prepend_text_for_markdown_file(now) + output_text
        print(f"Saving output to {md_path.absolute()}...")
        with open(str(md_path), 'w', encoding='utf-8') as f:
            f.write(output_text)

    def _prepend_text_for_markdown_file(self, now: str):

        prepend_text = f"# Root directory: {self.root_dir}  \n" \
                       f"# Included files: {self._included_file_extensions}  \n" \
                       f"Configurations: self.excuded_directories: {self._excluded_directories}  \n" \
                       f"self.included_file_types: {self._included_file_extensions}  \n"

        return prepend_text

    def _get_current_timestamp(self):
        now = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        return now


if __name__ == "__main__":
    # root_directory = input("Enter the root directory: ")
    # root_directory = r"C:\Users\jonma\github_repos\jonmatthis\golem_garden"
    # root_directory = r"C:\Users\jonma\github_repos\jonmatthis\Alpaca-Turbo"
    root_directory = r"C:\Users\jonma\obsidian_markdown\freemocap\documentation\docs\works_in_progress"
    excluded_directories = [".git",
                            ".idea",
                            "venv",
                            "utilities",
                            "tests",
                            "docs",
                            "data",
                            "golem_garden.egg-info",
                            ]
    included_file_extensions = [".py",
                                ".md", ]

    print(f"Printing the structure of {root_directory}...")
    walker = DirectoryWalker(root_dir=root_directory,
                             excluded_directories=excluded_directories,
                             included_file_extensions=included_file_extensions
                             )
    walker.print_structure()