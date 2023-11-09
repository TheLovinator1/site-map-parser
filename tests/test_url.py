from __future__ import annotations

import re
from datetime import datetime

import pytest

from sitemap_parser.url import Url


class TestUrl:
    """Test Url class."""

    def test_init_fully_loaded(self: TestUrl) -> None:
        """Test init.

        Args:
            self: TestUrl
        """
        priority = 0.3

        u = Url(
            loc="http://www.example2.com/index2.html",
            lastmod="2010-11-04T17:21:18+00:00",
            changefreq="never",
            priority=priority,
        )
        assert u.loc == "http://www.example2.com/index2.html"
        assert type(u.lastmod) is datetime
        assert str(u.lastmod) == "2010-11-04 17:21:18+00:00"
        assert u.changefreq == "never"
        assert type(u.priority) is float
        assert u.priority == priority

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

        with pytest.raises(
            ValueError,
            match=re.escape(
                "'foobar' is not an allowed value: ('always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never')",  # noqa: E501
            ),
        ):
            u.changefreq = "foobar"

    def test_priority(self: TestUrl) -> None:
        """Test priority.

        Args:
            self: TestUrl
        """
        priority06 = 0.6
        priority03 = 0.3
        priority00 = 0.0
        priority10 = 1.0

        u = Url(loc="http://www.example/com/index.html", priority=priority06)
        assert u.priority == priority06
        u.priority = priority03
        assert u.priority == priority03
        u.priority = priority00
        assert u.priority == priority00
        u.priority = priority10
        assert u.priority == priority10

        with pytest.raises(ValueError, match="'{}' is not between 0.0 and 1.0"):
            u.priority = 1.1  # Max is 1.0
        with pytest.raises(ValueError, match="'{}' is not between 0.0 and 1.0"):
            u.priority = -0.1  # Min is 0.0

    def test_str(self: TestUrl) -> None:
        """Test str.

        Args:
            self: TestUrl
        """
        s = Url(loc="http://www.example2.com/index2.html")
        assert str(s) == "http://www.example2.com/index2.html"
