from pyment import PyComment
import ast


def create_normalized_sample_stack(filepath_to_dataset, tmp_filepath, normalized_filepath, number_of_scripts=5000):
    with open(filepath_to_dataset, "r") as input_file:
        non_normalized_scripts = [next(input_file) for _ in range(number_of_scripts)]

    normalized_scripts = []
    for script in non_normalized_scripts:
        with open(tmp_filepath, "w") as tmp_file:
            script_dict = ast.literal_eval(script)
            tmp_file.write(script_dict['content'])
            docstring_converter = PyComment(tmp_filepath, output_style='google', convert_only=True)
            docstring_converter.proceed()
            list_from, list_to = docstring_converter.compute_before_after()
            script_dict['content'] = "".join(list_to)
            normalized_scripts.append(str(script_dict))
    print(len(normalized_scripts))
    with open(normalized_filepath, "w") as normalized_file:
        for line in normalized_scripts:
            normalized_file.write(line)
            normalized_file.write("\n")


create_normalized_sample_stack("/the_stack_filtered.txt",
                               "/Users/mikhail.malofeev/programm/ml/thesis/tmp_file_to_normalize",
                               "/datasets/the_stack_normalized_sample.txt")
