import csv
import io
from datetime import datetime

from ..exporter import Exporter
from ..sitemap import Sitemap
from ..url import Url


class CSVExporter(Exporter):
    short_name = "csv"

    def export_sitemaps(self):
        """
        returns csv data with format:
        url: string
        lastmod: ISO8601 format date
        """
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            delimiter=",",
            fieldnames=Sitemap.fields,
            quoting=csv.QUOTE_NONNUMERIC,
        )
        writer.writeheader()
        for sm in self.data.get_sitemaps():
            row = {}
            for field in Sitemap.fields:
                v = getattr(sm, field)
                row[field] = v if type(v) is not datetime else v.isoformat()
            writer.writerow(row)

        return buffer.getvalue().rstrip()

    def export_urls(self):
        """
        returns csv data with format:
        url: string
        lastmod: ISO8601 format date
        changefreq: string
        priority: float, 0-1
        """
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer, delimiter=",", fieldnames=Url.fields, quoting=csv.QUOTE_NONNUMERIC
        )
        writer.writeheader()
        for url in self.data.get_urls():
            row = {}
            for field in Url.fields:
                v = getattr(url, field)
                row[field] = v if type(v) is not datetime else v.isoformat()
            writer.writerow(row)

        return buffer.getvalue().rstrip()
