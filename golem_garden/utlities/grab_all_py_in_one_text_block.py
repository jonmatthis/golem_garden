import os
from pathlib import Path

repo_path = Path(__file__).parent.parent.parent
exclude_dirs = ['__pycache__', 'venv', 'build', 'dist', 'golem_garden.egg-info']
output = []
for root, dirs, files in os.walk(repo_path):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            output.append(f"### {file_path}\n")
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
                output.append(f"```python\n{file_content}\n```\n")

output_text = "\n".join(output)
print(f"\n\n\n{output_text}\n\n\n")
