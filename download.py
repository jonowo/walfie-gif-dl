import itertools
import json
import logging
import os.path
import re
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


with open("data.json", "r") as f:
    data = json.load(f)

# Download GIFs
logger.info(f"Downloading {len(data)} GIFs...")
for post in data:
    resp = requests.get(post["gif"])
    resp.raise_for_status()
    with open(get_filename(post["title"]), "wb") as f:
        f.write(resp.content)
    time.sleep(0.5)
logger.info("Download complete.")
