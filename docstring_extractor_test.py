import ast
from docstring_extractor import get_docstrings


def print_docstrings(node, script):
    if isinstance(node, ast.FunctionDef):
        text_body = ast.get_source_segment(script, node)
        print(text_body)
        print("_____________________________________________________")
        # print(node.body)
    for child in ast.iter_child_nodes(node):
        print_docstrings(child, script)

with open(".tmp", "r") as input_:
    content = input_.read()
    # docstrings = get_docstrings(input_)
    module = ast.parse(content)
    # function_definitions = [node for node in module.body if isinstance(node, ast.FunctionDef)]
    # for node in ast.iter_child_nodes(module):
    #     for child in ast.iter_child_nodes(node):
    #         print(child)
    # print(function_definitions)
    # print(docstrings)
    print_docstrings(module, content)


    
