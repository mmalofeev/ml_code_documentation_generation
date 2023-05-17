from datasets import load_dataset

def get_the_stack_repos():
    auth_token = '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'
    ds = load_dataset("bigcode/the-stack", data_dir="data/python", streaming=True, use_auth_token=auth_token,
                      split="train")
    count = 0
    set_of_repos = set()
    for sample in iter(ds):
        if count == 250000:
            return set_of_repos
        count += 1
        set_of_repos.add('http://github.com/' + sample['max_stars_repo_name'])

def print_dublicated_repos(filepath_input, filepath_output, set_of_repos):
    input = open(filepath_input, "r")
    output = open(filepath_output, "w")
    lines = input.readlines()
    for line in lines:
        repo_name = line.split()[1]
        if repo_name in set_of_repos:
            output.write(repo_name)
            output.write("\n")


def get_150k_repos(filepath):
    input = open(filepath, "r")
    lines = input.readlines()
    set_of_repos = set()
    for line in lines:
        repo_name = line.split()[1]
        set_of_repos.add(repo_name)
    return set_of_repos

def get_the_stack_filtered(filepath, set_of_existing_repos):
    output = open(filepath, "w")
    auth_token = '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'
    ds = load_dataset("bigcode/the-stack", data_dir="data/python", streaming=True, use_auth_token=auth_token,
                      split="train")
    count = 0
    for sample in iter(ds):
        if count == 250000:
            return
        repo_name = 'http://github.com/' + sample['max_stars_repo_name']
        if (repo_name not in set_of_existing_repos) and sample['max_stars_count'] is not None and sample['max_stars_count'] >= 500:
            output.write(str(sample))
            output.write("\n")
            count += 1
            print(count)
        # else:
            # print(repo_name)
    print()


filepath_input = "/Users/mikhail.malofeev/programm/ml/thesis/py150_files/github_repos.txt"
set_of_150k_repos = get_150k_repos(filepath_input)
filepath_output = "/Users/mikhail.malofeev/programm/ml/thesis/the_stack_filtered_huge.txt"
get_the_stack_filtered(filepath_output, set_of_150k_repos)


# set_of_repos = get_the_stack_repos()
# print("set of repos extracted")
# filepath_output = "/Users/mikhail.malofeev/programm/ml/thesis/dublicated_repos.txt"
# print("start to find dublicated repos")
# print_dublicated_repos(filepath_input, filepath_output, set_of_repos)
# print("dublicated repos found")
