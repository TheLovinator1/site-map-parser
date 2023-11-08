from datetime import datetime

import pytest

from sitemapparser.sitemap import Sitemap


class TestSitemap:
    def test_init(self):
        s = Sitemap(
            loc="http://www.example.com/index.html", lastmod="2004-10-01T18:24:19+00:00"
        )

        assert s.loc == "http://www.example.com/index.html"
        assert type(s.lastmod) == datetime
        assert s.lastmod.isoformat() == "2004-10-01T18:24:19+00:00"

    def test_str(self):
        s = Sitemap(
            loc="http://www.example.com/index.html", lastmod="2004-10-01T18:24:19+00:00"
        )
        assert str(s) == "http://www.example.com/index.html"
