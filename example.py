from __future__ import annotations

import sys

from loguru import logger

from sitemap_parser import SitemapIndex, SiteMapParser, UrlSet

# Set Loguru logger level to INFO
logger.remove()
logger.add(sys.stderr, level="INFO", colorize=True, format="{message}")

# Define a constant for the magic value
MAX_URLS_TO_DISPLAY = 10


def get_sitemaps() -> None:
    """Get the urls from a sitemap."""
    sm = SiteMapParser("https://sverigesradio.se/sitemap")
    sitemaps: SitemapIndex = sm.get_sitemaps()
    logger.info("Sitemaps:")
    for sitemap in sitemaps:
        # You can use get_urls() to get the urls from this sitemap.
        logger.info(f"\t{sitemap=}")

    sm2 = SiteMapParser("https://sverigesradio.se/sitemap?type=publish&id=0")
    sitemaps2: UrlSet = sm2.get_urls()

    logger.info("Urls:")
    for i, url in enumerate(sitemaps2):
        if i >= MAX_URLS_TO_DISPLAY:
            logger.info("\t... (truncated due to sitemap having 15 000 urls)")
            break
        logger.info(f"\t{url=}")


if __name__ == "__main__":
    get_sitemaps()
