import ast
import sys, token, tokenize

def delete_docstring(script, tmp_filepath1, tmp_filepath2):
    """ Run on just one file.

    """
    with open(tmp_filepath1, "w") as source:
        source.write(script)
    with open(tmp_filepath1, "r") as source:
        with open(tmp_filepath2, "w") as mod:

            prev_toktype = token.INDENT
            first_line = None
            last_lineno = -1
            last_col = 0

            tokgen = tokenize.generate_tokens(source.readline)
            for toktype, ttext, (slineno, scol), (elineno, ecol), ltext in tokgen:
                if 0:   # Change to if 1 to see the tokens fly by.
                    print("%10s %-14s %-20r %r" % (
                        tokenize.tok_name.get(toktype, toktype),
                        "%d.%d-%d.%d" % (slineno, scol, elineno, ecol),
                        ttext, ltext
                        ))
                if slineno > last_lineno:
                    last_col = 0
                if scol > last_col:
                    mod.write(" " * (scol - last_col))
                if not (toktype == token.STRING and prev_toktype == token.INDENT):
                    mod.write(ttext)
                prev_toktype = toktype
                last_col = ecol
                last_lineno = elineno
    result = ""
    with open(tmp_filepath2, "r") as mod:
        result = "".join(mod.readlines())
    return result

def processed_code_snippet(script, node, docstring, number_of_lines=50):
    new_script = script
    docstring_length = len(docstring.split("\n")) + 3
    func_length = node.end_lineno - node.lineno - docstring_length
    if func_length > number_of_lines:
        raise Exception("too big function!")
    # new_script = new_script.replace(docstring, "")
    new_script = delete_docstring(script, ".tmp1", ".tmp2")
    first_line = node.lineno - (number_of_lines - func_length)
    if first_line < 0:
        first_line = 0
    new_script = "\n".join(new_script.split("\n")[first_line:node.end_lineno - docstring_length])
    return new_script

def visit_node(script, node, dataset, data_sample_shown, count_unparsed):
    if isinstance(node, ast.FunctionDef):
        docstring = ast.get_docstring(node)
        if docstring is not None:
            try:
                if data_sample_shown[0] == False:
                    print("Code before preprocessing: ")
                    print("__________________________________________________")
                    print(script)
                snippet = processed_code_snippet(script, node, docstring)
                if data_sample_shown[0] == False:
                    print("__________________________________________________")
                    print("Code after preprocessing:")
                    print("__________________________________________________")
                    print(snippet)
                    data_sample_shown[0] = True
                dataset['input_ids'].append(snippet)
                dataset['labels'].append(docstring)

            except Exception as e:
                count_unparsed[0] += 1
                print(e)
    for child in ast.iter_child_nodes(node):
        visit_node(script, child, dataset, data_sample_shown, count_unparsed)

def get_training_dict(filepath):
    dataset_dict = {'input_ids': [], 'labels': []}
    count_unparsed = [0]
    count_parsed = 0
    with open(filepath, "r") as input:
        data_sample_shown = [False]
        lines = input.readlines()
        for line in lines:
            data = ast.literal_eval(line)
            script = data['content']
            try:
                node = ast.parse(script)
                visit_node(script, node, dataset_dict, data_sample_shown, count_unparsed)
                count_parsed += 1
            except:
                count_unparsed[0] += 1
    print("__________________________________________________")
    print(f"Scripts unable to parse: {count_unparsed[0]}")
    print(f"Scripts parsed: {count_parsed}")
    new_dataset = {'input_ids': dataset_dict['input_ids'][:5000], 'labels': dataset_dict['labels'][:5000]}
    return new_dataset

def get_dataset(filepath, new_dataset_filepath):
    dataset_dict = get_training_dict(filepath)
    with open(new_dataset_filepath, "w") as dataset:
        for script, docstring in zip(dataset_dict['input_ids'], dataset_dict['labels']):
            dataset.write("<s>\n")
            dataset.write("<code>\n")
            dataset.write(script)
            dataset.write("</code>\n")
            dataset.write("<docstring>\n")
            dataset.write(docstring)
            dataset.write("</docstring>\n")
            dataset.write("</s>\n")

if __name__ == '__main__':
     filepath = "../datasets/the_stack_normalized_sample.txt"
     new_dataset_filepath = "../datasets/the_stack_dataset_fine_tune_wrong.txt"
     get_dataset(filepath, new_dataset_filepath)