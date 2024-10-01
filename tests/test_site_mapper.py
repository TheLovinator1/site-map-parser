from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from lxml import etree

from sitemap_parser.sitemap_parser import SiteMapParser

if TYPE_CHECKING:
    from collections.abc import Iterator

    from pytest_httpx import HTTPXMock

    from sitemap_parser.sitemap import Sitemap
    from sitemap_parser.sitemap_index import SitemapIndex
    from sitemap_parser.url import Url
    from sitemap_parser.url_set import UrlSet


class TestSiteMapper:
    """Test the SiteMapper class."""

    def setup_method(self: TestSiteMapper) -> None:
        """Setup for TestSiteMapper.

        Args:
            self: TestSiteMapper
        """
        sitemap_index_data: bytes = Path.open(
            Path("tests/sitemap_index_data.xml"),
            "rb",
        ).read()
        utf8_parser = etree.XMLParser(encoding="utf-8")
        self.sitemap_index_xml_root = etree.parse(
            BytesIO(sitemap_index_data),
            parser=utf8_parser,
        ).getroot()
        self.sitemap_index_element_xml = self.sitemap_index_xml_root[0]

        url_set_data_bytes: bytes = Path.open(Path("tests/urlset_a.xml"), "rb").read()
        utf8_parser = etree.XMLParser(encoding="utf-8")
        self.url_set_data_xml = etree.parse(
            BytesIO(url_set_data_bytes),
            parser=utf8_parser,
        )
        self.url_set_element = self.url_set_data_xml.getroot()
        self.url_element_1 = self.url_set_data_xml.getroot()[0]

    def test_is_sitemap_index_element(self: TestSiteMapper) -> None:
        """Test is_sitemap_index_element.

        Args:
            self: TestSiteMapper
        """
        sitemap_index_result: bool = SiteMapParser._is_sitemap_index_element(  # noqa: SLF001
            self.sitemap_index_xml_root,
        )
        url_set_result: bool = SiteMapParser._is_sitemap_index_element(  # noqa: SLF001
            self.url_set_element,
        )
        assert sitemap_index_result is True
        assert url_set_result is False

    def test_is_url_set_element(self: TestSiteMapper) -> None:
        """Test is_url_set_element.

        Args:
            self: TestSiteMapper
        """
        url_set_result: bool = SiteMapParser._is_url_set_element(self.url_set_element)  # noqa: SLF001
        sitemap_index_result: bool = SiteMapParser._is_url_set_element(  # noqa: SLF001
            self.sitemap_index_xml_root,
        )
        assert url_set_result is True
        assert sitemap_index_result is False

    def test_get_sitemaps(self: TestSiteMapper, httpx_mock: HTTPXMock) -> None:
        """Test get_sitemaps."""
        amount_of_sitemaps: int = len(self.sitemap_index_xml_root)
        smi_data: bytes = Path.open(
            Path("tests/sitemap_index_data.xml"),
            "rb",
        ).read()
        httpx_mock.add_response(url="http://www.sitemap-example.com", content=smi_data)
        sm = SiteMapParser("http://www.sitemap-example.com")
        site_maps: SitemapIndex = sm.get_sitemaps()
        assert len(list(site_maps)) == amount_of_sitemaps

    def test_get_sitemaps_inappropriate_call(
        self: TestSiteMapper,
        httpx_mock: HTTPXMock,
    ) -> None:
        """Test get_sitemaps inappropriate call."""
        us_data: bytes = Path.open(Path("tests/urlset_a.xml"), "rb").read()
        httpx_mock.add_response(url="http://www.url-example.com", content=us_data)
        sm = SiteMapParser("http://www.url-example.com")
        with pytest.raises(KeyError):
            sm.get_sitemaps()

    def test_get_urls(self: TestSiteMapper, httpx_mock: HTTPXMock) -> None:
        """Test get_urls."""
        amount_of_urls: int = len(self.url_set_element)
        us_data: bytes = Path.open(Path("tests/urlset_a.xml"), "rb").read()
        httpx_mock.add_response(url="http://www.url-example.com", content=us_data)
        sm = SiteMapParser("http://www.url-example.com")
        url_set: UrlSet = sm.get_urls()
        assert len(list(url_set)) == amount_of_urls

    def test_get_urls_inappropriate_call(
        self: TestSiteMapper,
        httpx_mock: HTTPXMock,
    ) -> None:
        """Test get_urls inappropriate call."""
        smi_data: bytes = Path.open(
            Path("tests/sitemap_index_data.xml"),
            "rb",
        ).read()
        httpx_mock.add_response(url="http://www.sitemap-example.com", content=smi_data)
        smi = SiteMapParser("http://www.sitemap-example.com")
        with pytest.raises(KeyError):
            smi.get_urls()

    def test_has_sitemaps(self: TestSiteMapper, httpx_mock: HTTPXMock) -> None:
        """Test has_sitemaps."""
        smi_data: bytes = Path.open(
            Path("tests/sitemap_index_data.xml"),
            "rb",
        ).read()
        httpx_mock.add_response(url="http://www.sitemap-example.com", content=smi_data)
        sm = SiteMapParser("http://www.sitemap-example.com")
        assert sm.has_sitemaps() is True
        assert sm.has_urls() is False

    def test_has_urls(self: TestSiteMapper, httpx_mock: HTTPXMock) -> None:
        """Test has_urls."""
        us_data: bytes = Path.open(Path("tests/urlset_a.xml"), "rb").read()
        httpx_mock.add_response(url="http://www.url-example.com", content=us_data)
        sm = SiteMapParser("http://www.url-example.com")
        assert sm.has_urls() is True
        assert sm.has_sitemaps() is False

    def test_get_urls_multiple_iters(
        self: TestSiteMapper,
        httpx_mock: HTTPXMock,
    ) -> None:
        """Test get_urls multiple iters."""
        us_data: bytes = Path.open(Path("tests/urlset_a.xml"), "rb").read()
        httpx_mock.add_response(url="http://www.url-example.com", content=us_data)
        sm = SiteMapParser("http://www.url-example.com")
        urls_1: Iterator[Url] = iter(sm.get_urls())
        urls_2: Iterator[Url] = iter(sm.get_urls())
        assert str(next(urls_1)) == "http://www.example.com/page/a/1"
        assert str(next(urls_2)) == "http://www.example.com/page/a/1"
        assert str(next(urls_1)) == "http://www.example.com/page/a/2"
        assert str(next(urls_1)) == "http://www.example.com/page/a/3"

    def test_get_sitemaps_multiple_iters(
        self: TestSiteMapper,
        httpx_mock: HTTPXMock,
    ) -> None:
        """Test get_sitemaps multiple iters."""
        us_data: bytes = Path.open(
            Path("tests/sitemap_index_data.xml"),
            "rb",
        ).read()
        httpx_mock.add_response(url="http://www.url-example.com", content=us_data)
        sm = SiteMapParser("http://www.url-example.com")
        sm_1: Iterator[Sitemap] = iter(sm.get_sitemaps())
        sm_2: Iterator[Sitemap] = iter(sm.get_sitemaps())

        assert str(next(sm_1)) == "http://www.example.com/sitemap_a.xml"
        assert str(next(sm_1)) == "https://www.example.com/sitemap_b.xml"
        assert str(next(sm_2)) == "http://www.example.com/sitemap_a.xml"
