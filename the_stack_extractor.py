from  datasets  import  load_dataset

auth_token = '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'

ds = load_dataset("bigcode/the-stack", data_dir="data/python", streaming=True, use_auth_token=auth_token, split="train")

cnt = 0

for sample in iter(ds):
    cnt += 1
    if cnt < 5:
        continue
    print(sample)
    print(sample['content'])
    break
