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


def get_link_name(name) -> str:
    name = name.lower().replace(" ", "-")
    name = "".join(c if c.isalnum() or c in "-_" else "" for c in name)
    return name


with open(FN, "w") as f:
    print("# Categories", file=f)
    for tag in tags:
        print(f"- [{string.capwords(tag)}](#{get_link_name(tag)})", file=f)
    for tag in tags:
        print(file=f)
        print(f"## {string.capwords(tag)}", file=f)
        for post in categories[tag]:
            print(f'<img src="{post["path"]}" height="256">', file=f)
