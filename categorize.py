import json
import string
from datetime import datetime

FILENAME = "categories.md"
GIF_HEIGHT = 256

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

with open(FILENAME, "w") as f:
    print("# Categories", file=f)
    print(f"Last updated: {datetime.utcnow().replace(microsecond=0)} UTC", file=f)
    for tag in tags:
        print(file=f)
        print("<details>", file=f)
        print(f"    <summary>{string.capwords(tag)} ({len(categories[tag])})</summary>", file=f)
        for post in categories[tag]:
            print(f'    <img src="{post["path"]}" height="{GIF_HEIGHT}">', file=f)
        print("</details>", file=f)
