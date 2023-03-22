import os
from datetime import datetime
from pathlib import Path


class CodeDirectoryParser:
    """
    A class to parse a directory of code files and output them in a specified format.

    Args:
        directory_path (str): The path to the directory to parse.
        excluded_directories (list[str]): A list of directory names to exclude from parsing.
        included_file_types (list[str]): A list of file types to include in parsing.
        output_format (str): The format to output the parsed files. Either 'md' or 'text'.
    """

    def __init__(self, directory_path, excluded_directories=None, included_file_types=None, output_format='md'):
        self.directory_path = directory_path
        self.excluded_directories = excluded_directories or []
        self.included_file_types = included_file_types or []
        self.output_format = output_format
        self.output = []

    def parse_directory(self):
        """
        Parse the code directory and append the parsed files to the output.
        """
        for root, sub_directories, files in os.walk(self.directory_path):
            sub_directories[:] = [d for d in sub_directories if d not in self.excluded_directories]
            for file in files:
                if not self.included_file_types or file.endswith(tuple(self.included_file_types)):
                    file_path = os.path.join(root, file)
                    self.output.append(f"### {file_path}\n")
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        self.output.append(f"```python\n{file_content}\n```\n")

    def print_output(self):
        """
        Print the parsed output to the console or a file.
        """
        output_text = "\n".join(self.output)


        print(output_text)
        print("\n \n Done! \n \n")
        print(f"Output length: {len(output_text)}")
        if self.output_format == 'md':
            self._save_to_markdown_file(output_text)

    def _save_to_markdown_file(self, output_text):
        now = self._get_current_timestamp()
        md_path = Path(__file__).parent / "output" /  f"copy_of_directory_{Path(self.directory_path).name}_on_{now}_output.md"
        md_path.parent.mkdir(parents=True, exist_ok=True)
        output_text = self._prepend_text_for_markdown_file(now) + output_text
        print(f"Saving output to {md_path.absolute()}...")
        with open(str(md_path), 'w', encoding='utf-8') as f:
            f.write(output_text)

    def _prepend_text_for_markdown_file(self, now:str):

        prepend_text = f"# Copy of directory: {Path(self.directory_path).name} on {now}\n" \
                       f"Configurations: self.excuded_directories: {self.excluded_directories}, " \
                        f"self.included_file_types: {self.included_file_types} \n \n"
        return prepend_text

    def _get_current_timestamp(self):
        now = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        return now


if __name__ == '__main__':
    directory_path = r"C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\user_interface\web_app"

    excluded_directories = ['__pycache__',
                            'venv',
                            'build',
                            'dist',
                            'golem_garden.egg-info',
                            'tests',
                            'system',
                            'utilities',
                            'notes',
                            'experimental']

    included_file_types = ['.py', '.txt', '.md', '.html', '.css', '.js', '.json']

    parser = CodeDirectoryParser(directory_path, excluded_directories, included_file_types, output_format='md')
    parser.parse_directory()
    parser.print_output()
    print("Done!")