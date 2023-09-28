import json
import logging
import re
import html
from datetime import datetime

from httpx import Client

POSTS_PER_PAGE = 200
URL = "https://walfiegif.wordpress.com/"
POST_PATTERN = re.compile(r"<article.*?id=\"post-\d+\".*?>[\s\S]+?</article>")
IMAGE_PATTERN = re.compile(r"<img.*?src=\"(.*?)[\?|\"].*?>")
POST_URL_PATTERN = re.compile(r"<h1 class=\"entry-title\"><a href=\"(.*?)\".*?>")
TITLE_PATTERN = re.compile(r"<h1 class=\"entry-title\"><.*?>(.*?)<.*?>")
TAGS_PATTERN = re.compile(r"<a.*?rel=\"tag\".*?>(.*?)</a>")
DATE_PATTERN = re.compile(r"\d+/\d+/\d+")

logging.basicConfig(level="INFO", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


params = {
    "infinity": "scrolling",
    "page": 1,
    "query_args[posts_per_page]": POSTS_PER_PAGE
}
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
}
client = Client(headers=headers)


# Scrape data
logger.info("Scraping data...")
data = []
while True:
    r = client.post(URL, params=params)
    r = r.json()

    # Check if any posts there
    if r.get("type") != "success" or r.get("html") is None:
        break

    # Decode html entities to unicode
    raw_html = html.unescape(r.get("html"))

    posts = re.findall(POST_PATTERN, raw_html)
    for post in posts:
        post_url = re.search(POST_URL_PATTERN, post).group(1)
        gif_url = re.search(IMAGE_PATTERN, post).group(1)
        title = re.search(TITLE_PATTERN, post).group(1)

        tags = re.findall(TAGS_PATTERN, post)
        if not tags and title == "crunchy marshmallow":
            tags = [
                "amelia watson",
                "hololive"
            ]
            logger.info(f"Tags added manually for post {title!r}.")

        elif not tags:
            tags = []
            logger.warning(f"No tags found for post {title!r}.")

        date = re.search(DATE_PATTERN, post_url).group()
        date = datetime.strptime(date, "%Y/%m/%d").date()

        data.append({
            "post": post_url,
            "gif": gif_url,
            "title": title,
            "date": date,
            "tags": tags
        })

    # Move to next page
    params.update({"page": params.get("page") + 1})

with open("data.json", "w") as f:
    json.dump(data, f, indent=4, default=str)
logger.info("Stored data.")
