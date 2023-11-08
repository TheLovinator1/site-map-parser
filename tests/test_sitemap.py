from __future__ import annotations

from datetime import datetime

from sitemapparser.sitemap import Sitemap


class TestSitemap:
    """Test Sitemap class."""

    def test_init(self: TestSitemap) -> None:
        """Test Sitemap.__init__."""
        s = Sitemap(
            loc="http://www.example.com/index.html",
            lastmod="2004-10-01T18:24:19+00:00",
        )

        assert s.loc == "http://www.example.com/index.html"
        assert type(s.lastmod) is datetime
        assert s.lastmod.isoformat() == "2004-10-01T18:24:19+00:00"

    def test_str(self: TestSitemap) -> None:
        """Test Sitemap.__str__.

        Args:
            self: TestSitemap
        """
        s = Sitemap(
            loc="http://www.example.com/index.html",
            lastmod="2004-10-01T18:24:19+00:00",
        )
        assert str(s) == "http://www.example.com/index.html"
