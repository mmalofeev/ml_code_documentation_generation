import ast
from pyment import PyComment

tmp_filepath = "./tmp.txt"

def get_dataset_entry(data_string, dataset, unparsed):
    data = ast.literal_eval(data_string)
    script = data['original_string']
    try:
        with open(tmp_filepath, "w") as tmp_file:
            tmp_file.write(script)
        docstring_converter = PyComment(tmp_filepath, output_style='google', convert_only=True)
        docstring_converter.proceed()
        list_from, list_to = docstring_converter.compute_before_after()
        script = "".join(list_to)
        try:
            node = ast.parse(script)
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.FunctionDef):
                    docstring = ast.get_docstring(child)
                    script_without_docstrings = data['code']
                    if docstring is not None and len(docstring) > 0:
                        dataset['function'].append(script_without_docstrings)
                        dataset['docstring'].append(docstring)
        except:
            unparsed[0] += 1
    except:
        unparsed[0] += 1

def print_code_and_docstring(filepath, dataset_filepath):
    file = open(filepath, "r")
    jsons_strings = file.readlines()
    print(len(jsons_strings))
    count = 0
    unparsed = [0]
    dataset_dict = {'function': [], 'docstring': []}
    for json_string in jsons_strings:
        get_dataset_entry(json_string, dataset_dict, unparsed)
    print("Dataset has {} entries", len(dataset_dict['function']))
    print("{} functions was unparsed", unparsed[0])

    with open(dataset_filepath, "w") as dataset:
        for script, docstring in zip(dataset_dict['function'], dataset_dict['docstring']):
            dataset.write("<s>\n")
            dataset.write("<code>\n")
            dataset.write(script)
            dataset.write("\n</code>\n")
            dataset.write("<docstring>\n")
            dataset.write(docstring)
            dataset.write("\n</docstring>\n")
            dataset.write("</s>\n")

print_code_and_docstring("/Users/mikhail.malofeev/Downloads/docs/train/train_scenario_docs_chk_0.jsonl", "../datasets/pytorrent_dataset.txt")
