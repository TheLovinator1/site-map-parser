from __future__ import annotations

import csv
from unittest.mock import MagicMock

from sitemapparser.exporters.csv_exporter import CSVExporter
from sitemapparser.sitemap import Sitemap
from sitemapparser.url import Url


class TestExporter:
    """Test the CSV exporter."""

    def test_export_sitemaps(self: TestExporter) -> None:
        """Test the CSV exporter."""
        mock_site_mapper = MagicMock()
        mock_site_mapper.get_sitemaps = MagicMock(
            return_value=[
                Sitemap("http://www.example1.com"),
                Sitemap("http://www.example2.com", "2010-10-01T18:32:17+00:00"),
                Sitemap(
                    "http://www.example3.com/sitemap.xml",
                    "2010-10-01T18:32:17+00:00",
                ),
            ],
        )
        csv_exporter = CSVExporter(mock_site_mapper)
        csv_data: str = csv_exporter.export_sitemaps()
        csv_data_parsed = list(
            csv.DictReader(csv_data.split("\r\n"), quoting=csv.QUOTE_NONNUMERIC),
        )

        assert csv_data_parsed[0]["loc"] == "http://www.example1.com"
        assert not csv_data_parsed[0]["lastmod"]
        assert csv_data_parsed[1]["loc"] == "http://www.example2.com"
        assert csv_data_parsed[1]["lastmod"] == "2010-10-01T18:32:17+00:00"
        assert csv_data_parsed[2]["loc"] == "http://www.example3.com/sitemap.xml"
        assert csv_data_parsed[2]["lastmod"] == "2010-10-01T18:32:17+00:00"

    def test_export_urls(self: TestExporter) -> None:
        """Test the CSV exporter."""
        freq_08 = 0.8
        freq_09 = 0.9
        freq_10 = 1.0

        mock_url_set = MagicMock()
        mock_url_set.get_urls = MagicMock(
            return_value=[
                Url(
                    "http://www.example.com/page/a/1",
                    "2005-05-06",
                    "monthly",
                    freq_08,
                ),
                Url(
                    "http://www.example.com/page/a/2",
                    "2006-07-08",
                    "monthly",
                    freq_08,
                ),
                Url(
                    "http://www.example.com/page/a/3",
                    "2007-09-10",
                    "monthly",
                    freq_09,
                ),
                Url(
                    "http://www.example.com/page/a/4",
                    "2008-11-12",
                    "monthly",
                    freq_10,
                ),
            ],
        )
        csv_exporter = CSVExporter(mock_url_set)
        csv_data = csv_exporter.export_urls()
        csv_data_parsed = list(
            csv.DictReader(csv_data.split("\r\n"), quoting=csv.QUOTE_NONNUMERIC),
        )

        assert csv_data_parsed[0]["loc"] == "http://www.example.com/page/a/1"
        assert csv_data_parsed[0]["lastmod"] == "2005-05-06T00:00:00"
        assert csv_data_parsed[0]["changefreq"] == "monthly"
        assert csv_data_parsed[0]["priority"] == freq_08
        assert csv_data_parsed[1]["loc"] == "http://www.example.com/page/a/2"
        assert csv_data_parsed[1]["lastmod"] == "2006-07-08T00:00:00"
        assert csv_data_parsed[1]["changefreq"] == "monthly"
        assert csv_data_parsed[1]["priority"] == freq_08
        assert csv_data_parsed[2]["loc"] == "http://www.example.com/page/a/3"
        assert csv_data_parsed[2]["lastmod"] == "2007-09-10T00:00:00"
        assert csv_data_parsed[2]["changefreq"] == "monthly"
        assert csv_data_parsed[2]["priority"] == freq_09
        assert csv_data_parsed[3]["loc"] == "http://www.example.com/page/a/4"
        assert csv_data_parsed[3]["lastmod"] == "2008-11-12T00:00:00"
        assert csv_data_parsed[3]["changefreq"] == "monthly"
        assert csv_data_parsed[3]["priority"] == freq_10
