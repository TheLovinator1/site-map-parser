from __future__ import annotations

from datetime import datetime

import pytest

from sitemapparser.url import Url


class TestUrl:
    """Test Url class."""

    def test_init_fully_loaded(self: TestUrl) -> None:
        """Test init.

        Args:
            self: TestUrl
        """
        u = Url(
            loc="http://www.example2.com/index2.html",
            lastmod="2010-11-04T17:21:18+00:00",
            changefreq="never",
            priority=0.3,
        )
        assert u.loc == "http://www.example2.com/index2.html"
        assert type(u.lastmod) is datetime
        assert str(u.lastmod) == "2010-11-04 17:21:18+00:00"
        assert u.changefreq == "never"
        assert type(u.priority) is float
        assert u.priority == 0.3  # noqa: PLR2004

    def test_changefreq(self: TestUrl) -> None:
        """Test changefreq.

        Args:
            self: TestUrl
        """
        u = Url(loc="http://www.example.com/index.html", changefreq="always")
        assert u.changefreq == "always"
        u.changefreq = None
        assert u.changefreq is None
        u.changefreq = "hourly"
        assert u.changefreq == "hourly"
        u.changefreq = "daily"
        assert u.changefreq == "daily"
        u.changefreq = "weekly"
        assert u.changefreq == "weekly"
        u.changefreq = "monthly"
        assert u.changefreq == "monthly"
        u.changefreq = "yearly"
        assert u.changefreq == "yearly"
        u.changefreq = "never"
        assert u.changefreq == "never"

        with pytest.raises(ValueError):  # noqa: PT011
            u.changefreq = "foobar"

    def test_priority(self: TestUrl) -> None:
        """Test priority.

        Args:
            self: TestUrl
        """
        u = Url(loc="http://www.example/com/index.html", priority=0.6)
        assert u.priority == 0.6  # noqa: PLR2004
        u.priority = 0.3
        assert u.priority == 0.3  # noqa: PLR2004
        u.priority = 0.0
        assert u.priority == 0.0  # noqa: PLR2004
        u.priority = 1.0
        assert u.priority == 1.0  # noqa: PLR2004

        with pytest.raises(ValueError):  # noqa: PT011
            u.priority = 1.1
        with pytest.raises(ValueError):  # noqa: PT011
            u.priority = -0.1

    def test_str(self: TestUrl) -> None:
        """Test str.

        Args:
            self: TestUrl
        """
        s = Url(loc="http://www.example2.com/index2.html")
        assert str(s) == "http://www.example2.com/index2.html"
