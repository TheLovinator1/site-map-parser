from __future__ import annotations

import logging

from sitemap_parser import SitemapIndex, SiteMapParser, UrlSet

# Set up logging
logger: logging.Logger = logging.getLogger(__name__)


def get_sitemaps() -> None:
    """Get the urls from a sitemap."""
    sitemap = SiteMapParser("https://sverigesradio.se/sitemap")
    sitemaps: SitemapIndex = sitemap.get_sitemaps()
    logger.info("Sitemaps:")
    for sitemap in sitemaps:
        # You can use get_urls() to get the urls from this sitemap.
        logger.info(f"\t{sitemap=}")

    second_sitemap = SiteMapParser("https://sverigesradio.se/sitemap?type=publish&id=0")
    extracted_urls: UrlSet = second_sitemap.get_urls()

    logger.info("Urls:")
    for i, url in enumerate(extracted_urls):
        max_urls_to_display = 10
        if i >= max_urls_to_display:
            logger.info("\t... (truncated due to sitemap having 15 000 urls)")
            break
        logger.info(f"\t{url=}")

    logger.info("Done.")


if __name__ == "__main__":
    get_sitemaps()
