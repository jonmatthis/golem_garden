import ast

def extract_functions(node):
    if isinstance(node, ast.FunctionDef):
        inputs = [arg.arg for arg in node.args.args]
        output = node.returns.id if node.returns else None
        print(f"Function: {node.name}, Inputs: {inputs}, Output: {output}")
    elif isinstance(node, ast.AsyncFunctionDef):
        inputs = [arg.arg for arg in node.args.args]
        output = node.returns.id if node.returns else None
        print(f"Async Function: {node.name}, Inputs: {inputs}, Output: {output}")

def extract_classes(node):
    if isinstance(node, ast.ClassDef):
        print(f"Class: {node.name}")
        for subnode in node.body:
            extract_functions(subnode)

def extract_from_file(filename):
    with open(filename, "r") as file:
        source = file.read()
    tree = ast.parse(source)
    for node in tree.body:
        extract_classes(node)
        extract_functions(node)

if __name__ == "__main__":
    script_path = r"C:\Users\jonma\github_repos\jonmatthis\golem_garden\golem_garden\__main__.py"
    extract_from_file(script_path)
