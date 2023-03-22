import asyncio
import logging
import re
import sys
from typing import IO

import aiofiles
import aiohttp
from aiohttp import ClientSession

import urllib.error
import urllib.parse

# config logging
logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

# re to find href links
HREF_RE = re.compile(r'href="(.*?)"')

async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """
    Get request wrapper to fetch_html
    :param url: url to fetch
    :param session: ClientSession instance
    :param kwargs: kwargs to pass to `session.request()`
    :return: html text
    """
    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    html = await resp.text()
    return html

async def parse(url: str, session: ClientSession, **kwargs) -> set:
    """
    Find all href links in html
    :param url: url to fetch
    :param session: ClientSession instance
    :param kwargs: kwargs to pass to `session.request()`
    :return: set of href links
    """
    found = set()
    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError
    ) as e:
        logger.error(f"Error fetching {url}: {e}")
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occurred %s", getattr(e, "__dict__", {})
        )
    else:
        for link in HREF_RE.findall(html): 
            try:
                abslink = urllib.parse.urljoin(url, link)
            except (urllib.error.URLError, ValueError) as e:
                logger.exception("Error parsing %s: %s", link, e)
            else:
                found.add(abslink)
    logger.info("Found %d links for %s", len(found), url)
    return found

async def write_one(file: IO, url: str, **kwargs) -> None:
    """
    Write url to file
    :param file: file-like object to write to
    :param url: url to write
    :return: None
    """
    res = await parse(url=url, **kwargs)
    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        for p in res:
            await f.write(f"{url} -> {p}\n")
        logger.info("Wrote %d links for %s", len(res), url)
    
async def main(file: IO, urls: set, **kwargs) -> None:
    """
    Entry point for the program
    """
    async with ClientSession() as session:
        tasks = []
        for u in urls:
            tasks.append(
                write_one(file=file, url=u, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    import pathlib
    import sys

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
    here = pathlib.Path(__file__).parent

    with open(here / "urls.txt") as f:
        urls = set(map(str.strip, f))
    
    outpath = here / "foundurls.txt"
    with open(outpath, 'w') as f:
        f.write("source -> target\n")
    asyncio.run(main(file=outpath, urls=urls))
