from __future__ import annotations

import json
from unittest.mock import MagicMock

from sitemapparser.exporters.json_exporter import JSONExporter
from sitemapparser.sitemap import Sitemap
from sitemapparser.url import Url


class TestExporter:
    """Test the JSON exporter."""

    def test_export_sitemaps(self: TestExporter) -> None:
        """Test the JSON exporter.

        Args:
            self: TestExporter
        """
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
        json_exporter = JSONExporter(mock_site_mapper)
        json_data: str = json_exporter.export_sitemaps()
        json_data_parsed = json.loads(json_data)

        assert len(json_data_parsed) == 3  # noqa: PLR2004
        assert json_data_parsed[0]["loc"] == "http://www.example1.com"
        assert json_data_parsed[1]["loc"] == "http://www.example2.com"
        assert str(json_data_parsed[1]["lastmod"]) == "2010-10-01T18:32:17+00:00"
        assert json_data_parsed[2]["loc"] == "http://www.example3.com/sitemap.xml"
        assert str(json_data_parsed[2]["lastmod"]) == "2010-10-01T18:32:17+00:00"

    def test_export_urls(self: TestExporter) -> None:
        """Test the JSON exporter.

        Args:
            self: TestExporter
        """
        mock_url_set = MagicMock()
        mock_url_set.get_urls = MagicMock(
            return_value=[
                Url(
                    "http://www.example.com/page/a/1",
                    "2005-05-06T00:00:00",
                    "monthly",
                    0.8,
                ),
                Url(
                    "http://www.example.com/page/a/2",
                    "2006-07-08T00:00:00",
                    "monthly",
                    0.8,
                ),
                Url(
                    "http://www.example.com/page/a/3",
                    "2007-09-10T00:00:00",
                    "monthly",
                    0.9,
                ),
                Url(
                    "http://www.example.com/page/a/4",
                    "2008-11-12T00:00:00",
                    "monthly",
                    1.0,
                ),
            ],
        )
        json_exporter = JSONExporter(mock_url_set)
        json_data = json_exporter.export_urls()
        json_data_parsed = json.loads(json_data)

        assert len(json_data_parsed) == 4  # noqa: PLR2004
        assert json_data_parsed[0]["loc"] == "http://www.example.com/page/a/1"
        assert str(json_data_parsed[0]["lastmod"]) == "2005-05-06T00:00:00"
        assert json_data_parsed[0]["changefreq"] == "monthly"
        assert json_data_parsed[0]["priority"] == 0.8  # noqa: PLR2004
        assert json_data_parsed[1]["loc"] == "http://www.example.com/page/a/2"
        assert str(json_data_parsed[1]["lastmod"]) == "2006-07-08T00:00:00"
        assert json_data_parsed[1]["changefreq"] == "monthly"
        assert json_data_parsed[1]["priority"] == 0.8  # noqa: PLR2004
        assert json_data_parsed[2]["loc"] == "http://www.example.com/page/a/3"
        assert str(json_data_parsed[2]["lastmod"]) == "2007-09-10T00:00:00"
        assert json_data_parsed[2]["changefreq"] == "monthly"
        assert json_data_parsed[2]["priority"] == 0.9  # noqa: PLR2004
        assert json_data_parsed[3]["loc"] == "http://www.example.com/page/a/4"
        assert str(json_data_parsed[3]["lastmod"]) == "2008-11-12T00:00:00"
        assert json_data_parsed[3]["changefreq"] == "monthly"
        assert json_data_parsed[3]["priority"] == 1.0  # noqa: PLR2004
