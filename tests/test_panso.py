import json
from typing import TYPE_CHECKING

from sitemap_parser.exporter import JSONExporter
from sitemap_parser.sitemap_parser import SiteMapParser

if TYPE_CHECKING:
    from sitemap_parser.sitemap_index import SitemapIndex
    from sitemap_parser.url_set import UrlSet


def test_panso() -> None:
    """Test panso."""
    sm = SiteMapParser("https://panso.se/sitemap.xml")
    if sm.has_sitemaps():
        sitemaps: SitemapIndex = sm.get_sitemaps()
        assert sitemaps is not None
    else:
        urls: UrlSet = sm.get_urls()
        assert urls is not None

    json_exporter = JSONExporter(sm)
    if sm.has_sitemaps():
        sitemaps_json: str = json_exporter.export_sitemaps()
        assert sitemaps_json is not None
        assert json.loads(sitemaps_json) is not None

    elif sm.has_urls():
        urls_json: str = json_exporter.export_urls()
        assert urls_json is not None
        assert json.loads(urls_json) is not None
