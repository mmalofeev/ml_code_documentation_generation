def parse_file_to_array(filepath):
    with open(filepath, "r") as input:
        lines = input.readlines()
        dataset_entries = {'input': [], 'gold_ref': []}
        start = 0
        end = 0
        count = 0
        while end != len(lines):
            code = start
            end_code = start
            while lines[code] != "<code>\n":
                code += 1
            while lines[end_code] != "</code>\n":
                end_code += 1
            if end_code - code <= 2:
                count += 1
            while lines[start] != "<s>\n":
                start += 1
            docstring_line = start
            while lines[docstring_line] != "<docstring>\n":
                docstring_line += 1
            while lines[end] != "</s>\n":
                end += 1
            entry = "".join(lines[docstring_line + 1:end - 1])
            input = "".join(lines[start:docstring_line + 1])

            dataset_entries['input'].append(input)
            dataset_entries['gold_ref'].append(entry)
            start += 1
            end += 1
    return count

count = parse_file_to_array("/Users/mikhail.malofeev/programm/ml/thesis/datasets/the_stack_dataset_fine_tune_huge.txt")

print(count)
