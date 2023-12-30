import asyncio
import itertools
import json
import logging
import os
import re
import shutil
from typing import Iterable

from httpx import AsyncClient, TimeoutException

DOWNLOAD_PATH = "gifs/"
TIMEOUT = 5

logging.basicConfig(level="INFO", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def get_filename(name) -> str:
    # Sanitize filename
    fn = "".join(c if c.isalnum() else "_" for c in name)
    fn = re.sub("_+", "_", fn)
    ext = ".gif"

    # Find next available filename
    path = DOWNLOAD_PATH + fn + ext
    if not os.path.exists(path):
        return path

    for i in itertools.count(1):
        path = DOWNLOAD_PATH + fn + str(i) + ext
        if not os.path.exists(path):
            return path


async def download(client: AsyncClient, post: dict) -> None:
    """Download GIFs"""
    try:
        resp = await client.get(post["gif"])
        resp.raise_for_status()
    except TimeoutException as e:
        logger.warning(f"{e} for {post['url']}. Waiting for {TIMEOUT} s.")
        await asyncio.sleep(TIMEOUT)
        return await download(client, post)
    else:
        fn = get_filename(post["title"])
        post["path"] = fn

        with open(fn, "wb") as f:
            f.write(resp.content)


async def download_chunk(posts: Iterable[dict]) -> None:
    async with AsyncClient() as client:
        await asyncio.gather(*[download(client, post) for post in posts])


if os.path.isdir(DOWNLOAD_PATH):
    shutil.rmtree(DOWNLOAD_PATH)
os.mkdir(DOWNLOAD_PATH)

with open("data.json") as f:
    data = json.load(f)

chunk_size = 10
logger.info(f"Downloading {len(data)} GIFs...")
# Download older posts first to make sure their file names are not taken
data = data[::-1]
for chunk_start in range(0, len(data), chunk_size):
    data_chunk = data[chunk_start:chunk_start+chunk_size]
    asyncio.run(download_chunk(data_chunk))
    logger.info(f"{chunk_start + len(data_chunk)}/{len(data)} GIFs downloaded.")
data = data[::-1]

logger.info("Download complete.")

with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
