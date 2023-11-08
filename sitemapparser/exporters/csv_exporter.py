from __future__ import annotations

import csv
import io
from datetime import datetime

from sitemapparser.exporter import Exporter
from sitemapparser.sitemap import Sitemap
from sitemapparser.url import Url


class CSVExporter(Exporter):
    """Export site map data to CSV format.

    Args:
        Exporter: Base class for all exporters

    Returns:
        CSV data
    """

    short_name = "csv"  # type: ignore  # noqa: PGH003

    def export_sitemaps(self: CSVExporter) -> str:
        """Export site map data to CSV format.

        Returns:
            CSV data
        """
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            delimiter=",",
            fieldnames=Sitemap.fields,
            quoting=csv.QUOTE_NONNUMERIC,
        )
        writer.writeheader()
        for sm in self.data.get_sitemaps():  # type: ignore  # noqa: PGH003
            row = {}
            for field in Sitemap.fields:
                v = getattr(sm, field)
                row[field] = v if type(v) is not datetime else v.isoformat()
            writer.writerow(row)

        return buffer.getvalue().rstrip()

    def export_urls(self: CSVExporter) -> str:
        """Export site map data to CSV format.

        Returns csv data with format:
            url: string
            lastmod: ISO8601 format date
            changefreq: string
            priority: float, 0-1

        Returns:
            CSV data
        """
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            delimiter=",",
            fieldnames=Url.fields,
            quoting=csv.QUOTE_NONNUMERIC,
        )
        writer.writeheader()
        for url in self.data.get_urls():  # type: ignore  # noqa: PGH003
            row = {}
            for field in Url.fields:
                v = getattr(url, field)
                row[field] = v if type(v) is not datetime else v.isoformat()
            writer.writerow(row)

        return buffer.getvalue().rstrip()
