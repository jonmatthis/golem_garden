import os
import sys
import inspect
import importlib.util
from typing import Union
from rich import print, inspect as rich_inspect


def print_object_info(obj: Union[object, str], print_code: bool = False):
    if isinstance(obj, str):
        spec = importlib.util.spec_from_file_location("module.name", obj)
        obj = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = obj
        spec.loader.exec_module(obj)

    print(f"File: {inspect.getfile(obj)}\n")

    for name, cls in inspect.getmembers(obj, inspect.isclass):
        print(f"Class: {name}\n")

        for method_name, method in inspect.getmembers(cls, inspect.isfunction):
            rich_inspect(method, methods=True, docs=True, private=True)
            if print_code:
                print("Code:")
                print(inspect.getsource(method))

    for function_name, function in inspect.getmembers(obj, inspect.isfunction):
        rich_inspect(function, methods=True)

        if print_code:
            print("Code:")
            print(inspect.getsource(function))


if __name__ == "__main__":
    # Example usage
    script_path = r"/golem_garden/__main__.py"
    print_code = False  # Set to True to print the related Python code

    print_object_info(script_path, print_code)
