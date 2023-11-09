import json
import sys
from typing import TYPE_CHECKING

from loguru import logger

from sitemap_parser.exporter import JSONExporter
from sitemap_parser.sitemap_parser import SiteMapParser

if TYPE_CHECKING:
    from sitemap_parser.sitemap_index import SitemapIndex
    from sitemap_parser.url_set import UrlSet

# Set Loguru logger level to INFO
logger.remove()
logger.add(sys.stderr, level="INFO", colorize=True, format="{message}")


def get_sitemaps() -> None:
    """If we want to get the sitemaps from another sitemap, we can do it like this."""
    sm = SiteMapParser("https://www.webhallen.com/sitemap.xml")
    if sm.has_sitemaps():
        # This will alway be true because the sitemap at https://www.webhallen.com/sitemap.xml has other sitemaps inside it. # noqa: E501

        # Get the sitemaps inside the sitemap at https://www.webhallen.com/sitemap.xml
        sitemaps: SitemapIndex = sm.get_sitemaps()
        logger.info("Sitemaps:")
        for sitemap in sitemaps:
            logger.info(f"\t{sitemap=}")
            # sitemap will be like this:
            # sitemap=<Sitemap https://www.webhallen.com/sitemap.home.xml>
            # sitemap=<Sitemap https://www.webhallen.com/sitemap.section.xml>
            # sitemap=<Sitemap https://www.webhallen.com/sitemap.category.xml>
            # sitemap=<Sitemap https://www.webhallen.com/sitemap.campaign.xml>
            # sitemap=<Sitemap https://www.webhallen.com/sitemap.campaignList.xml>
            # sitemap=<Sitemap https://www.webhallen.com/sitemap.infoPages.xml>
            # sitemap=<Sitemap https://www.webhallen.com/sitemap.product.xml>
            # sitemap=<Sitemap https://www.webhallen.com/sitemap.manufacturer.xml>
            # sitemap=<Sitemap https://www.webhallen.com/sitemap.article.xml>


def get_urls() -> None:
    """Get the urls from a sitemap."""
    sm = SiteMapParser("https://www.webhallen.com/sitemap.article.xml")
    urls: UrlSet = sm.get_urls()
    for url in urls:
        logger.info(f"{url=}")
        # Result:
        """url=Url(loc='https://panso.se/', lastmod=datetime.datetime(2023, 11, 8, 0, 0), changefreq='daily', priority=0.5)"""  # noqa: E501

    json_exporter = JSONExporter(sm)
    if sm.has_sitemaps():
        sitemaps_json: str = json_exporter.export_sitemaps()
        logger.info(f"{sitemaps_json=}")

    elif sm.has_urls():
        urls_json: str = json_exporter.export_urls()
        logger.info(f"{urls_json=}")

        # Result:
        """urls_json = [
                {
                    "loc": "https://panso.se/",
                    "lastmod": "2023-11-08T00:00:00",
                    "changefreq": "daily",
                    "priority": 0.5,
                },
                {
                    "loc": "https://panso.se/webhallen/",
                    "lastmod": "2023-11-08T00:00:00",
                    "changefreq": "daily",
                    "priority": 0.5,
                },
                {
                    "loc": "https://panso.se/api/docs",
                    "lastmod": null,
                    "changefreq": "daily",
                    "priority": 0.5,
                },
            ]
        """


def get_json() -> None:
    """Same as above but with json."""
    sm = SiteMapParser("https://www.webhallen.com/sitemap.article.xml")
    json_exporter = JSONExporter(sm)
    if sm.has_sitemaps():
        sitemaps_json: str = json_exporter.export_sitemaps()
        logger.info(f"{sitemaps_json=}")

    elif sm.has_urls():
        urls_json: str = json_exporter.export_urls()
        urls_json = json.loads(urls_json)
        logger.info(json.dumps(urls_json, indent=4))

        # Result:
        """
        [
            {
                "loc": "https://www.webhallen.com/se/article/2-Covid-19-Butiksatgarder",
                "lastmod": null,
                "changefreq": null,
                "priority": 0.3
            },
            {
                "loc": "https://www.webhallen.com/se/article/4-Tre-enkla-steg-for-ett-smart-hem",
                "lastmod": null,
                "changefreq": null,
                "priority": 0.3
            },
            ... truncated ...
        ]
        """


if __name__ == "__main__":
    get_urls()
    get_sitemaps()
    get_json()
