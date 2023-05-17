import ast
def get_training_data(filepath):
    dataset_dict = {'input_ids': [], 'labels': []}
    count_unparsed = 0
    count_parsed = 0
    with open(filepath, "r") as input:
        data_sample_shown = [False]
        lines = input.readlines()
        count = 0
        for line in lines:
            data = ast.literal_eval(line)
            count += 1
            script = data['content']
            if count == 3:
                print(data)
                break

get_training_data("../datasets/the_stack_normalized_dataset_without_new_lines.txt")