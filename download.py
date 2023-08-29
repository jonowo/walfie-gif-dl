import itertools
import json
import logging
import os
import re
import shutil
import time

import requests

DOWNLOAD_PATH = "gifs/"

logging.basicConfig(level="INFO", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_filename(name) -> str:
    # Sanitize filename
    fn = "".join(c if c.isalnum() else "_" for c in name)
    fn = re.sub("_+", "_", fn)
    ext = ".gif"

    # Find next available filename
    if not os.path.exists(DOWNLOAD_PATH + fn + ext):
        return DOWNLOAD_PATH + fn + ext
    for i in itertools.count(1):
        if not os.path.exists(DOWNLOAD_PATH + fn + str(i) + ext):
            return DOWNLOAD_PATH + fn + str(i) + ext


if os.path.isdir(DOWNLOAD_PATH):
    shutil.rmtree(DOWNLOAD_PATH)
os.mkdir(DOWNLOAD_PATH)

with open("data.json") as f:
    data = json.load(f)

# Download GIFs
logger.info(f"Downloading {len(data)} GIFs...")
# Download older posts first to make sure their file names are not taken
for post in data[::-1]:
    resp = requests.get(post["gif"])
    resp.raise_for_status()
    fn = get_filename(post["title"])
    post["path"] = fn
    with open(fn, "wb") as f:
        f.write(resp.content)
    time.sleep(5)
logger.info("Download complete.")

with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
