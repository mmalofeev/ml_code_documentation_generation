from pyment import PyComment

with open("tmp_pyment.txt", "w") as tmp_file:
    docstring_converter = PyComment("script.txt", output_style='google', convert_only=True)
    docstring_converter.proceed()
    list_from, list_to = docstring_converter.compute_before_after()
    tmp_file.write("".join(list_to))