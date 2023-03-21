import os
import pathlib
import ast
import toml

def get_functions(filename):
    with open(filename, "r") as file:
        try:
            source = file.read()
            module = ast.parse(source)
        except SyntaxError:
            return []
        functions = []
        for node in module.body:
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                defaults = [None] * (len(args) - len(node.args.defaults)) + node.args.defaults if node.args.defaults else []
                parameters = dict(zip(args, defaults))
                for arg in node.args.kwonlyargs:
                    if arg.arg not in parameters:
                        parameters[arg.arg] = None
                for arg in node.args.vararg, node.args.kwarg:
                    if arg and arg.arg not in parameters:
                        parameters[arg.arg] = None
                if node.returns:
                    returns = ast.dump(node.returns)
                else:
                    returns = "None"
                functions.append((node.name, parameters, returns))
        return functions

def crawl_directory(root_dir, exclude=None):
    exclude = exclude or []
    for path in pathlib.Path(root_dir).rglob("*"):
        if path.is_dir():
            if any([dirname in path.parts for dirname in exclude]):
                continue
            print("Directory:", path)
        elif path.is_file():
            print("File:", path)
            if path.suffix == ".py":
                functions = get_functions(path)
                if functions:
                    print("Functions:")
                    for name, parameters, returns in functions:
                        print("\t" + name + "(" + ", ".join([f"{arg}={repr(default)}" for arg, default in parameters.items()]) + f") -> {returns}")
            elif path.suffix == ".toml":
                with open(path, "r") as file:
                    data = toml.load(file)
                print("TOML contents:", data)

root_dir = r"C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden"
exclude = [".git", "venv", "build", "dist", "golem_garden.egg-info", ".vscode", "golem_garden.egg-info", "__pycache__"]
crawl_directory(root_dir, exclude)
