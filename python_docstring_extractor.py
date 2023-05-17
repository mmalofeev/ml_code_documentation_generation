from docstring_extractor import get_docstrings


def extract_docstrings(path_file_with_paths):
    file_with_paths = open(path_file_with_paths, "r")
    paths_to_files = file_with_paths.readlines()
    count = 0
    path_to_file_with_files_with_docstrings = "./docstrings_files.txt"
    file_with_files_with_docstrings = open(path_to_file_with_files_with_docstrings, "w")
    for line in paths_to_files:
        file_path = "./py150_files/" + line[:-1]
        python_script = open(file_path, "r")
        try:
            docstrings = get_docstrings(python_script)
            for function in docstrings["content"]:
                if len(function["docstring_text"]) != 0 or len(docstrings["docstring_text"]) != 0:
                    file_with_files_with_docstrings.write(line)
                    break
        except:
            count += 1
            print("Error while parsing " + file_path)

    print(count)
extract_docstrings("/Users/mikhail.malofeev/programm/ml/thesis/py150_files/python100k_train.txt")
