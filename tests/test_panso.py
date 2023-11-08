import json
from typing import TYPE_CHECKING

from sitemapparser.exporters.csv_exporter import CSVExporter
from sitemapparser.exporters.json_exporter import JSONExporter
from sitemapparser.site_map_parser import SiteMapParser

if TYPE_CHECKING:
    from sitemapparser.sitemap_index import SitemapIndex
    from sitemapparser.url_set import UrlSet


def test_panso() -> None:
    """Test panso."""
    sm = SiteMapParser("https://panso.se/sitemap.xml")
    if sm.has_sitemaps():
        sitemaps: SitemapIndex = sm.get_sitemaps()
        assert sitemaps is not None
    else:
        urls: UrlSet = sm.get_urls()
        assert urls is not None

    csv_exporter = CSVExporter(sm)  # type: ignore  # noqa: PGH003
    if sm.has_sitemaps():
        sitemaps_csv: str = csv_exporter.export_sitemaps()
        assert sitemaps_csv is not None
    elif sm.has_urls():
        urls_csv: str = csv_exporter.export_urls()
        assert urls_csv is not None

    json_exporter = JSONExporter(sm)  # type: ignore  # noqa: PGH003
    if sm.has_sitemaps():
        sitemaps_json: str = json_exporter.export_sitemaps()
        assert sitemaps_json is not None
        assert json.loads(sitemaps_json) is not None

    elif sm.has_urls():
        urls_json: str = json_exporter.export_urls()
        assert urls_json is not None
        assert json.loads(urls_json) is not None
