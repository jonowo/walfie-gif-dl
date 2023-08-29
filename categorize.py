import json
import string
from datetime import datetime

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
    print("Last updated:", str(datetime.utcnow().replace(microsecond=0)), "UTC", file=f)
    for tag in tags:
        print(file=f)
        print("<details>", file=f)
        print(f"    <summary>{string.capwords(tag)} ({len(categories[tag])})</summary>", file=f)
        for post in categories[tag]:
            print(f'    <img src="{post["path"]}" height="256">', file=f)
        print("</details>", file=f)
