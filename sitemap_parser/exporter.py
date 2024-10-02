from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from json import dumps
from typing import TYPE_CHECKING, Any, Literal

from sitemap_parser.sitemap import Sitemap
from sitemap_parser.url import Url

if TYPE_CHECKING:
    from sitemap_parser.sitemap_index import SitemapIndex
    from sitemap_parser.sitemap_parser import SiteMapParser
    from sitemap_parser.url_set import UrlSet

UrlFields = tuple[Literal["loc"], Literal["lastmod"], Literal["changefreq"], Literal["priority"]]
SitemapFields = tuple[Literal["loc"], Literal["lastmod"]]


@dataclass(slots=True)
class JSONExporter:
    """Export site map data to JSON format."""

    data: SiteMapParser

    @staticmethod
    def _collate(fields: SitemapFields | UrlFields, row_data: SitemapIndex | UrlSet) -> list[dict[str, Any]]:
        """Collate data from SitemapIndex or UrlSet into a list of dictionaries.

        Args:
            fields (tuple): A tuple of field names to extract from each Sitemap or Url object.
            row_data (SitemapIndex | UrlSet): An iterable containing Sitemap or Url objects.

        Returns:
            list: A list of dictionaries where each dictionary represents a Sitemap or Url object.
        """
        dump_data: list[dict[str, Any]] = []
        for sm in row_data:
            row: dict[str, Any] = {}
            for field in fields:
                v = getattr(sm, field)
                row[field] = v if not isinstance(v, datetime) else v.isoformat()
            dump_data.append(row)
        return dump_data

    def export_sitemaps(self: JSONExporter) -> str:
        """Export site map data to JSON format.

        Returns:
            JSON data as a string

        Returns:
            JSON data as a string
        """
        try:
            sitemap_fields: SitemapFields = getattr(Sitemap, "fields", ("loc", "lastmod"))  # Default fields
        except AttributeError:
            sitemap_fields: SitemapFields = ("loc", "lastmod")  # Default fields

        return dumps(self._collate(sitemap_fields, self.data.get_sitemaps()))

    def export_urls(self: JSONExporter) -> str:
        """Export site map data to JSON format.

        Returns:
            JSON data as a string
        """
        try:
            url_fields: UrlFields = getattr(Url, "fields", ("loc", "lastmod", "changefreq", "priority"))
        except AttributeError:
            url_fields: UrlFields = ("loc", "lastmod", "changefreq", "priority")  # Default fields

        return dumps(self._collate(url_fields, self.data.get_urls()))
