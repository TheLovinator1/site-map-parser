from __future__ import annotations

from datetime import datetime
from json import dumps

from sitemapparser.exporter import Exporter
from sitemapparser.sitemap import Sitemap
from sitemapparser.url import Url


class JSONExporter(Exporter):
    """Export site map data to JSON format.

    Args:
        Exporter: Base class for all exporters

    Returns:
        JSON data
    """

    short_name = "json"  # type: ignore  # noqa: PGH003

    def _collate(self: JSONExporter, fields: tuple, row_data: list) -> list:  # noqa: PLR6301
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
        return dumps(self._collate(Sitemap.fields, self.data.get_sitemaps()))  # type: ignore  # noqa: PGH003

    def export_urls(self: JSONExporter) -> str:
        """Export site map data to JSON format.

        Returns:
            JSON data
        """
        return dumps(self._collate(Url.fields, self.data.get_urls()))  # type: ignore  # noqa: PGH003
