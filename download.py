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
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)


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


async def download(client: AsyncClient, post: dict) -> None:
    """Download GIFs"""
    # Download older posts first to make sure their file names are not taken
    try:
        resp = await client.get(post["gif"])
        resp.raise_for_status()

    except TimeoutException as e:
        logger.warning(f"{e} for {post['url']}. Waiting for {TIMEOUT}")
        await asyncio.sleep(TIMEOUT)
        return await download(client, post)

    else:
        fn = get_filename(post["title"])
        post["path"] = fn

        with open(fn, "wb") as f:
            f.write(resp.content)


async def download_bunch(posts: Iterable[dict]) -> None:
    async with AsyncClient() as client:
        await asyncio.gather(*[download(client, post) for post in posts])


if os.path.isdir(DOWNLOAD_PATH):
    shutil.rmtree(DOWNLOAD_PATH)
os.mkdir(DOWNLOAD_PATH)

with open("data.json") as f:
    data = json.load(f)

chunk_size = 10
logger.info(f"Downloading {len(data)} GIFs...")
for chunk in range(0, len(data), chunk_size):
    data_chunk = data[chunk:chunk+chunk_size]
    asyncio.run(download_bunch(data_chunk))
    logger.info(f"{chunk + len(data_chunk)}/{len(data)} Downloaded")
logger.info("Download complete.")

with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
