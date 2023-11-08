from __future__ import annotations

from sitemapparser.smapper_utils import uri_modifier


def test_uri_modifier_begins() -> None:
    """Test uri_modifier."""
    test_url1 = "example.com"
    assert uri_modifier(test_url1) == "http://example.com/sitemap.xml"
    test_url2 = "http://www.example.com"
    assert uri_modifier(test_url2) == "http://www.example.com/sitemap.xml"


def test_uri_modifier_ends() -> None:
    """Test uri_modifier."""
    test_url1 = "http://www.example.com"
    assert uri_modifier(test_url1) == "http://www.example.com/sitemap.xml"
    test_url2 = "http://www.example.com/"
    assert uri_modifier(test_url2) == "http://www.example.com/sitemap.xml"
    test_url3 = "http://www.example.com/sitemap.xml"
    assert uri_modifier(test_url3) == "http://www.example.com/sitemap.xml"
