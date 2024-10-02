from __future__ import annotations

from sitemap_parser.smapper_utils import ensure_sitemap_url_format


def test_uri_modifier_begins() -> None:
    """Test uri_modifier."""
    test_url1 = "example.com"
    assert ensure_sitemap_url_format(test_url1) == "https://example.com/sitemap.xml"
    test_url2 = "http://www.example.com"
    assert ensure_sitemap_url_format(test_url2) == "http://www.example.com/sitemap.xml"


def test_uri_modifier_ends() -> None:
    """Test uri_modifier."""
    test_url1 = "http://www.example.com"
    assert ensure_sitemap_url_format(test_url1) == "http://www.example.com/sitemap.xml"
    test_url2 = "http://www.example.com/"
    assert ensure_sitemap_url_format(test_url2) == "http://www.example.com/sitemap.xml"
    test_url3 = "http://www.example.com/sitemap.xml"
    assert ensure_sitemap_url_format(test_url3) == "http://www.example.com/sitemap.xml"
