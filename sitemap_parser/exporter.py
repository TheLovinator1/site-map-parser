from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from json import dumps
from typing import TYPE_CHECKING

from sitemap_parser.sitemap import Sitemap
from sitemap_parser.url import Url

if TYPE_CHECKING:
    from sitemap_parser.sitemap_index import SitemapIndex
    from sitemap_parser.sitemap_parser import SiteMapParser
    from sitemap_parser.url_set import UrlSet


@dataclass
class JSONExporter:
    """Export site map data to JSON format.

    Args:
        Exporter: Base class for all exporters

    Returns:
        JSON data
    """

    data: SiteMapParser

    @staticmethod
    def _collate(fields: tuple, row_data: SitemapIndex | UrlSet) -> list:
        dump_data = []
        for sm in row_data:
            row = {}
            for field in fields:
                v = getattr(sm, field)
                row[field] = v if type(v) is not datetime else v.isoformat()
            dump_data.append(row)
        return dump_data

    def export_sitemaps(self: JSONExporter) -> str:
        """Export site map data to JSON format.

        Returns:
            JSON data
        """
        return dumps(self._collate(Sitemap.fields, self.data.get_sitemaps()))

    def export_urls(self: JSONExporter) -> str:
        """Export site map data to JSON format.

        Returns:
            JSON data
        """
        return dumps(self._collate(Url.fields, self.data.get_urls()))
