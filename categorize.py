import json
import string

FN = "categories.md"

with open("data.json") as f:
    data = json.load(f)

tags = set()
for post in data:
    tags |= set(post["tags"])
tags = sorted(tags)

categories = {tag: [] for tag in tags}
for post in data:
    for tag in post["tags"]:
        categories[tag].append(post)

with open(FN, "w") as f:
    print("# Categories", file=f)
    for tag in tags:
        print(f"- [{string.capwords(tag)}](#{tag.lower().replace(' ', '-')})", file=f)
    for tag in tags:
        print(file=f)
        print(f"## {string.capwords(tag)}", file=f)
        for post in categories[tag]:
            print(f'<img src="{post["path"]}" height="256">', file=f)
