from typing import TYPE_CHECKING

from loguru import logger

from sitemapparser.exporter import JSONExporter
from sitemapparser.site_map_parser import SiteMapParser

if TYPE_CHECKING:
    from sitemapparser.sitemap_index import SitemapIndex
    from sitemapparser.url_set import UrlSet


def main() -> None:
    """Get the sitemap from panso.se and export it to CSV and JSON."""
    sm = SiteMapParser("https://panso.se/sitemap.xml")
    if sm.has_sitemaps():
        sitemaps: SitemapIndex = sm.get_sitemaps()
        logger.info(f"{sitemaps=}")
    else:
        urls: UrlSet = sm.get_urls()
        logger.info(f"{urls=}")

    json_exporter = JSONExporter(sm)
    if sm.has_sitemaps():
        sitemaps_json: str = json_exporter.export_sitemaps()
        logger.info(f"{sitemaps_json=}")

    elif sm.has_urls():
        urls_json: str = json_exporter.export_urls()
        logger.info(f"{urls_json=}")


if __name__ == "__main__":
    main()
