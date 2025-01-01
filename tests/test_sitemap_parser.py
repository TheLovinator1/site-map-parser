from __future__ import annotations

import re
import typing
from datetime import datetime, timezone
from io import BytesIO
from json import dumps
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal
from unittest.mock import MagicMock

import hishel
import pytest
from lxml import etree
from pytest_httpx import HTTPXMock

from sitemap_parser import (
    BaseData,
    JSONExporter,
    Sitemap,
    SitemapIndex,
    SiteMapParser,
    Url,
    UrlSet,
    bytes_to_element,
    download_uri_data,
)

if TYPE_CHECKING:
    from collections.abc import Generator, Iterator
    from xml.etree.ElementTree import Element

    from pytest_httpx import HTTPXMock


# Sample data for testing
valid_sitemap_xml = """
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-01</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://example.com/about</loc>
    <lastmod>2024-01-02</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
"""

valid_sitemap_index_xml = """
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap1.xml</loc>
    <lastmod>2024-01-01</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap2.xml</loc>
    <lastmod>2024-01-02</lastmod>
  </sitemap>
</sitemapindex>
"""
sitemap_data: list[Sitemap] = [
    Sitemap(loc="https://example.com/sitemap1.xml", lastmod=datetime(2023, 1, 1, tzinfo=timezone.utc).isoformat()),
    Sitemap(loc="https://example.com/sitemap2.xml", lastmod=datetime(2023, 1, 2, tzinfo=timezone.utc).isoformat()),
]

url_data: list[Url] = [
    Url(
        loc="https://example.com/page1",
        lastmod=datetime(2023, 1, 1, tzinfo=timezone.utc).isoformat(),
        changefreq="daily",
        priority=1.0,
    ),
    Url(
        loc="https://example.com/page2",
        lastmod=datetime(2023, 1, 2, tzinfo=timezone.utc).isoformat(),
        changefreq="weekly",
        priority=0.8,
    ),
]


def test_parse_valid_sitemap() -> None:
    # Simulate parsing a valid sitemap XML string
    parser = SiteMapParser(source=valid_sitemap_xml, is_data_string=True)
    url_set = parser.get_urls()
    urls = list(url_set)

    assert len(urls) == 2
    assert urls[0].loc == "https://example.com/"
    assert urls[0].lastmod is not None
    assert urls[0].lastmod.isoformat() == "2024-01-01T00:00:00"
    assert urls[0].changefreq == "daily"
    assert urls[0].priority == 0.8


def test_parse_valid_sitemap_index() -> None:
    parser = SiteMapParser(source=valid_sitemap_index_xml, is_data_string=True)
    sitemap_index = parser.get_sitemaps()
    sitemaps = list(sitemap_index)

    assert len(sitemaps) == 2
    assert sitemaps[0].loc == "https://example.com/sitemap1.xml"
    assert sitemaps[0].lastmod is not None
    assert sitemaps[0].lastmod.isoformat() == "2024-01-01T00:00:00"


def test_invalid_url() -> None:
    # Test URL validation in Url class
    with pytest.raises(ValueError, match="invalid-url is not a valid URL"):
        Url(loc="invalid-url")  # Invalid URL should raise a ValueError


def test_changefreq_validation() -> None:
    with pytest.raises(
        expected_exception=ValueError,
        match=re.escape(
            pattern="'invalid' is not an allowed value: ('always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never')",  # noqa: E501
        ),
    ):
        Url(loc="https://example.com", changefreq="invalid")  # Invalid changefreq should raise a ValueError


def test_priority_validation() -> None:
    with pytest.raises(ValueError, match=r"'1.5' is not between 0.0 and 1.0"):
        Url(loc="https://example.com", priority=1.5)  # Priority outside of 0.0 - 1.0 range should raise a ValueError


def test_sitemap_object() -> None:
    # Test creating a Sitemap object
    sitemap = Sitemap(loc="https://example.com/sitemap1.xml", lastmod="2024-01-01")
    assert sitemap.loc == "https://example.com/sitemap1.xml"
    assert sitemap.lastmod is not None
    assert sitemap.lastmod.isoformat() == "2024-01-01T00:00:00"


def test_url_object() -> None:
    # Test creating a Url object
    url = Url(loc="https://example.com/", lastmod="2024-01-01", changefreq="daily", priority=0.8)
    assert url.loc == "https://example.com/"
    assert url.lastmod is not None
    assert url.lastmod.isoformat() == "2024-01-01T00:00:00"
    assert url.changefreq == "daily"
    assert url.priority == 0.8


def test_bytes_to_element() -> None:
    element = bytes_to_element(valid_sitemap_xml.encode("utf-8"))
    assert isinstance(element, etree._Element)  # type: ignore  # noqa: PGH003


def test_lastmod_value_correct() -> None:
    """Test lastmod value."""
    s1 = BaseData()
    s1.lastmod = "2019-12-01T01:33:35+00:00"

    s2 = BaseData()
    s2.lastmod = "2019-11-11T00:00:00+00:00"
    assert type(s1.lastmod) is datetime
    assert s1.lastmod == datetime(2019, 12, 1, 1, 33, 35, tzinfo=timezone.utc)
    assert type(s2.lastmod) is datetime
    assert s2.lastmod == datetime(2019, 11, 11, 0, 0, 0, tzinfo=timezone.utc)


def test_lastmod_value_incorrect() -> None:
    """Test lastmod value."""
    s1 = BaseData()
    # tests invalid month value
    with pytest.raises(ValueError, match=r"month must be in 1..12"):
        s1.lastmod = "2019-13-01T01:33:35+00:00"


def test_loc_value_correct() -> None:
    """Test loc value."""
    s1 = BaseData()
    s2 = BaseData()
    s1.loc = "http://www.example.com"
    s2.loc = "https://www.example.com/file.xml"

    assert s1.loc == "http://www.example.com"
    assert s2.loc == "https://www.example.com/file.xml"


def test_loc_value_incorrect() -> None:
    """Test loc value."""
    s = BaseData()
    with pytest.raises(ValueError, match=r"www.example.com is not a valid URL"):
        s.loc = "www.example.com"


def test_download_uri_data_sitemap_index(httpx_mock: HTTPXMock) -> None:
    """Test download_uri_data() with a sitemap index."""
    smi_data: bytes = Path.open(Path("tests/sitemap_index_data.xml"), "rb").read()
    httpx_mock.add_response(
        url="http://www.example.com/sitemapindex.xml",
        content=smi_data,
    )
    downloaded_data: bytes = download_uri_data(
        uri="http://www.example.com/sitemapindex.xml",
        should_cache=False,
    )
    assert downloaded_data == smi_data


def test_download_uri_data_sitemap_index_cache(httpx_mock: HTTPXMock) -> None:
    """Test download_uri_data() with a sitemap index with caching."""
    smi_data: bytes = Path.open(Path("tests/sitemap_index_data.xml"), "rb").read()
    httpx_mock.add_response(
        url="http://www.example.com/sitemapindex.xml",
        content=smi_data,
    )
    downloaded_data: bytes = download_uri_data(
        uri="http://www.example.com/sitemapindex.xml",
        hishel_client=hishel.CacheClient(),
        should_cache=True,
    )
    assert downloaded_data == smi_data


def test_download_uri_data_urlset(httpx_mock: HTTPXMock) -> None:
    """Test download_uri_data() with a urlset."""
    us_data = Path.open(Path("tests/urlset_a.xml"), "rb").read()
    httpx_mock.add_response(
        url="http://www.example.com/urlset_a.xml",
        content=us_data,
    )
    downloaded_data: bytes = download_uri_data(
        uri="http://www.example.com/urlset_a.xml",
        should_cache=False,
    )
    assert downloaded_data == us_data


def test_download_uri_data_urlset_cache(httpx_mock: HTTPXMock) -> None:
    """Test download_uri_data() with a urlset."""
    us_data = Path.open(Path("tests/urlset_a.xml"), "rb").read()
    httpx_mock.add_response(
        url="http://www.example.com/urlset_a.xml",
        content=us_data,
    )
    downloaded_data: bytes = download_uri_data(
        uri="http://www.example.com/urlset_a.xml",
        hishel_client=hishel.CacheClient(),
        should_cache=True,
    )
    assert downloaded_data == us_data


def test_data_to_element_sitemap_index() -> None:
    """Test data_to_element() with a sitemap index."""
    smi_data: bytes = Path.open(Path("tests/sitemap_index_data.xml"), "rb").read()
    root_element: Element = bytes_to_element(smi_data)
    assert len(root_element.xpath("/*[local-name()='sitemapindex']")) == 1  # type: ignore  # noqa: PGH003
    assert len(root_element.xpath("/*[local-name()='urlset']")) == 0  # type: ignore  # noqa: PGH003


def test_data_to_element_sitemap_index_broken() -> None:
    """Test data_to_element() with a broken sitemap index."""
    smi_data: bytes = Path.open(
        Path("tests/sitemap_index_data_broken.xml"),
        "rb",
    ).read()
    with pytest.raises(SyntaxError):
        bytes_to_element(smi_data)
    # assert len(root_element.xpath("/*[local-name()='sitemapindex']")) == 1
    # assert len(root_element.xpath("/*[local-name()='urlset']")) == 0


def test_data_to_element_urlset() -> None:
    """Test data_to_element() with a urlset."""
    us_data: bytes = Path.open(Path("tests/urlset_a.xml"), "rb").read()
    root_element: Element = bytes_to_element(us_data)
    assert len(root_element.xpath("/*[local-name()='sitemapindex']")) == 0  # type: ignore  # noqa: PGH003
    assert len(root_element.xpath("/*[local-name()='urlset']")) == 1  # type: ignore  # noqa: PGH003


class TestSiteMapper:
    """Test the SiteMapper class."""

    def setup_method(self: TestSiteMapper) -> None:
        """Setup for TestSiteMapper.

        Args:
            self: TestSiteMapper
        """
        sitemap_index_data: bytes = Path.open(Path("tests/sitemap_index_data.xml"), "rb").read()
        utf8_parser = etree.XMLParser(encoding="utf-8")
        self.sitemap_index_xml_root = etree.parse(BytesIO(sitemap_index_data), parser=utf8_parser).getroot()
        self.sitemap_index_element_xml = self.sitemap_index_xml_root[0]

        url_set_data_bytes: bytes = Path.open(Path("tests/urlset_a.xml"), "rb").read()
        utf8_parser = etree.XMLParser(encoding="utf-8")
        self.url_set_data_xml = etree.parse(BytesIO(url_set_data_bytes), parser=utf8_parser)
        self.url_set_element = self.url_set_data_xml.getroot()
        self.url_element_1 = self.url_set_data_xml.getroot()[0]

    def test_is_sitemap_index_element(self: TestSiteMapper) -> None:
        """Test is_sitemap_index_element.

        Args:
            self: TestSiteMapper
        """
        sitemap_index_result: bool = SiteMapParser._is_sitemap_index_element(  # pyright: ignore[reportPrivateUsage]
            typing.cast("Element", self.sitemap_index_xml_root),
        )
        url_set_result: bool = SiteMapParser._is_sitemap_index_element(typing.cast("Element", self.url_set_element))  # pyright: ignore[reportPrivateUsage]
        assert sitemap_index_result
        assert not url_set_result

    def test_is_url_set_element(self: TestSiteMapper) -> None:
        """Test is_url_set_element.

        Args:
            self: TestSiteMapper
        """
        url_set_result: bool = SiteMapParser._is_url_set_element(typing.cast("Element", self.url_set_element))  # pyright: ignore[reportPrivateUsage]
        sitemap_index_result: bool = SiteMapParser._is_url_set_element(  # pyright: ignore[reportPrivateUsage]
            typing.cast("Element", self.sitemap_index_xml_root),
        )
        assert url_set_result
        assert not sitemap_index_result

    def test_get_sitemaps(self: TestSiteMapper, httpx_mock: HTTPXMock) -> None:
        """Test get_sitemaps."""
        amount_of_sitemaps: int = len(self.sitemap_index_xml_root)
        smi_data: bytes = Path.open(Path("tests/sitemap_index_data.xml"), "rb").read()
        httpx_mock.add_response(url="http://www.sitemap-example.com", content=smi_data)
        sm = SiteMapParser("http://www.sitemap-example.com")
        site_maps: SitemapIndex = sm.get_sitemaps()
        assert len(list(site_maps)) == amount_of_sitemaps

    def test_get_sitemaps_inappropriate_call(self: TestSiteMapper, httpx_mock: HTTPXMock) -> None:
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

    def test_get_urls_inappropriate_call(self: TestSiteMapper, httpx_mock: HTTPXMock) -> None:
        """Test get_urls inappropriate call."""
        smi_data: bytes = Path.open(Path("tests/sitemap_index_data.xml"), "rb").read()
        httpx_mock.add_response(url="http://www.sitemap-example.com", content=smi_data)
        smi = SiteMapParser("http://www.sitemap-example.com")
        with pytest.raises(KeyError):
            smi.get_urls()

    def test_has_sitemaps(self: TestSiteMapper, httpx_mock: HTTPXMock) -> None:
        """Test has_sitemaps."""
        smi_data: bytes = Path.open(Path("tests/sitemap_index_data.xml"), "rb").read()
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

    def test_get_urls_multiple_iters(self: TestSiteMapper, httpx_mock: HTTPXMock) -> None:
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

    def test_get_sitemaps_multiple_iters(self: TestSiteMapper, httpx_mock: HTTPXMock) -> None:
        """Test get_sitemaps multiple iters."""
        us_data: bytes = Path.open(Path("tests/sitemap_index_data.xml"), "rb").read()
        httpx_mock.add_response(url="http://www.url-example.com", content=us_data)
        sm = SiteMapParser("http://www.url-example.com")
        sm_1: Iterator[Sitemap] = iter(sm.get_sitemaps())
        sm_2: Iterator[Sitemap] = iter(sm.get_sitemaps())

        assert str(next(sm_1)) == "http://www.example.com/sitemap_a.xml"
        assert str(next(sm_1)) == "https://www.example.com/sitemap_b.xml"
        assert str(next(sm_2)) == "http://www.example.com/sitemap_a.xml"


class TestSitemapIndex:
    """Test the SitemapIndex class."""

    def setup_method(self: TestSitemapIndex) -> None:
        """Setup for TestSitemapIndex."""
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

    def test_sitemap_from_sitemap_element(self: TestSitemapIndex) -> None:
        """Test sitemap_from_sitemap_element.

        Args:
            self: TestSitemapIndex
        """
        sm: Sitemap = SitemapIndex.sitemap_from_sitemap_element(typing.cast("Element", self.sitemap_index_element_xml))
        assert isinstance(sm, Sitemap)
        assert sm.loc == "http://www.example.com/sitemap_a.xml"
        assert type(sm.lastmod) is datetime
        assert str(sm.lastmod) == "2004-10-01 18:23:17+00:00"

    def test_sitemaps_from_sitemap_index_element(self: TestSitemapIndex) -> None:
        """Test sitemaps_from_sitemap_index_element.

        Args:
            self: TestSitemapIndex
        """
        amount_of_sitemaps: int = len(self.sitemap_index_xml_root)
        si: Generator[Sitemap, Any, None] = SitemapIndex.sitemaps_from_sitemap_index_element(
            typing.cast("Element", self.sitemap_index_xml_root),
        )
        assert len(list(si)) == amount_of_sitemaps

    def test_init(self: TestSitemapIndex) -> None:
        """Test init.

        Args:
            self: TestSitemapIndex
        """
        amount_of_sitemaps: int = len(self.sitemap_index_xml_root)
        smi = SitemapIndex(typing.cast("Element", self.sitemap_index_xml_root))
        assert len(list(smi)) == amount_of_sitemaps


class TestSitemap:
    """Test Sitemap class."""

    def test_init(self: TestSitemap) -> None:
        """Test Sitemap.__init__."""
        s = Sitemap(loc="http://www.example.com/index.html", lastmod="2004-10-01T18:24:19+00:00")

        assert s.loc == "http://www.example.com/index.html"
        assert type(s.lastmod) is datetime
        assert s.lastmod.isoformat() == "2004-10-01T18:24:19+00:00"

    def test_str(self: TestSitemap) -> None:
        """Test Sitemap.__str__.

        Args:
            self: TestSitemap
        """
        s = Sitemap(loc="http://www.example.com/index.html", lastmod="2004-10-01T18:24:19+00:00")
        assert str(s) == "http://www.example.com/index.html"


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

        with pytest.raises(ValueError, match=r"'1.1' is not between 0.0 and 1.0"):
            u.priority = 1.1  # Max is 1.0
        with pytest.raises(ValueError, match=r"'-0.1' is not between 0.0 and 1.0"):
            u.priority = -0.1  # Min is 0.0

    def test_str(self: TestUrl) -> None:
        """Test str.

        Args:
            self: TestUrl
        """
        s = Url(loc="http://www.example2.com/index2.html")
        assert str(s) == "http://www.example2.com/index2.html"


class TestUrlSet:
    """Test the UrlSet class."""

    def setup_method(self: TestUrlSet) -> None:
        """Setup for TestUrlSet."""
        url_set_data_bytes: bytes = Path.open(Path("tests/urlset_a.xml"), "rb").read()
        utf8_parser = etree.XMLParser(encoding="utf-8")
        self.url_set_data_xml = etree.parse(BytesIO(url_set_data_bytes), parser=utf8_parser)
        self.url_set_element = self.url_set_data_xml.getroot()
        self.url_element_1 = self.url_set_data_xml.getroot()[0]
        self.url_element_2 = self.url_set_data_xml.getroot()[1]

        # custom element handling
        custom_ele_file = "tests/urlset_a_custom_element.xml"
        url_set_custom_ele_bytes: bytes = Path.open(Path(custom_ele_file), "rb").read()
        self.url_set_data_custom_xml = etree.parse(BytesIO(url_set_custom_ele_bytes), parser=utf8_parser)
        self.url_set_custom_element = self.url_set_data_custom_xml.getroot()
        self.url_element_3 = self.url_set_data_custom_xml.getroot()[0]

    def test_allowed_fields(self: TestUrlSet) -> None:
        """Test allowed_fields."""
        for f in UrlSet.allowed_fields:
            assert f in {"loc", "lastmod", "changefreq", "priority"}

    def test_url_from_url_element(self: TestUrlSet) -> None:
        """Test url_from_url_element.

        Args:
            self: TestUrlSet
        """
        priority = 0.8
        url: Url = UrlSet.url_from_url_element(typing.cast("Element", self.url_element_1))
        assert isinstance(url, Url)
        assert url.loc == "http://www.example.com/page/a/1"
        assert type(url.lastmod) is datetime
        assert str(url.lastmod) == "2005-01-01 00:00:00"
        assert url.changefreq == "monthly"
        assert url.priority == priority

    def test_url_from_custom_url_element(self: TestUrlSet) -> None:
        """Test url_from_url_element.

        Args:
            self: TestUrlSet
        """
        priority = 0.3
        url: Url = UrlSet.url_from_url_element(typing.cast("Element", self.url_element_3))
        assert isinstance(url, Url)
        assert url.loc == "http://www.example.com/page/a/4"
        assert type(url.lastmod) is datetime
        assert str(url.lastmod) == "2006-05-05 00:00:00"
        assert url.changefreq == "monthly"
        assert url.priority == priority

    def test_urls_from_url_set_element(self: TestUrlSet) -> None:
        """Test urls_from_url_set_element.

        Args:
            self: TestUrlSet
        """
        amount_of_urls: int = len(self.url_set_element)
        urls: Generator[Url, Any, None] = UrlSet.urls_from_url_set_element(typing.cast("Element", self.url_set_element))
        assert len(list(urls)) == amount_of_urls

    def test_urls_from_url_set_custom_element(self: TestUrlSet) -> None:
        """Test urls_from_url_set_element.

        Args:
            self: TestUrlSet
        """
        urls: Generator[Url, Any, None] = UrlSet.urls_from_url_set_element(
            typing.cast("Element", self.url_set_custom_element),
        )
        assert len(list(urls)) == 1

    def test_init(self: TestUrlSet) -> None:
        """Test init.

        Args:
            self: TestUrlSet
        """
        amount_of_urls: int = len(self.url_set_element)
        u = UrlSet(typing.cast("Element", self.url_set_element))
        assert len(list(u)) == amount_of_urls


# Define sample data for testing


@pytest.fixture
def sitemap_parser_mock() -> MagicMock:
    """Fixture that mocks the SiteMapParser and its methods.

    Returns:
        MagicMock: Mocked SiteMapParser object
    """
    mock = MagicMock()
    mock.get_sitemaps.return_value = sitemap_data
    mock.get_urls.return_value = url_data
    return mock


def test_json_exporter_initialization(sitemap_parser_mock: MagicMock) -> None:
    """Test that the JSONExporter initializes properly with site map data."""
    exporter = JSONExporter(sitemap_parser_mock)
    assert exporter.data == sitemap_parser_mock


def test_collate_method_for_sitemaps(sitemap_parser_mock: MagicMock) -> None:
    """Test the _collate method for Sitemap objects."""
    exporter = JSONExporter(sitemap_parser_mock)
    fields: tuple[Literal["loc"], Literal["lastmod"]] = ("loc", "lastmod")

    expected_output: list[dict[str, str]] = [
        {"loc": "https://example.com/sitemap1.xml", "lastmod": "2023-01-01T00:00:00+00:00"},
        {"loc": "https://example.com/sitemap2.xml", "lastmod": "2023-01-02T00:00:00+00:00"},
    ]

    result: list[dict[str, Any]] = exporter._collate(fields, sitemap_data)  # type: ignore[arg-type]
    assert result == expected_output


def test_collate_method_for_urls(sitemap_parser_mock: MagicMock) -> None:
    """Test the _collate method for Url objects."""
    exporter = JSONExporter(sitemap_parser_mock)
    fields = ("loc", "lastmod", "changefreq", "priority")

    expected_output = [
        {
            "loc": "https://example.com/page1",
            "lastmod": "2023-01-01T00:00:00+00:00",
            "changefreq": "daily",
            "priority": 1.0,
        },
        {
            "loc": "https://example.com/page2",
            "lastmod": "2023-01-02T00:00:00+00:00",
            "changefreq": "weekly",
            "priority": 0.8,
        },
    ]

    result = exporter._collate(fields, url_data)  # type: ignore[arg-type]
    assert result == expected_output


def test_export_sitemaps(sitemap_parser_mock: MagicMock) -> None:
    """Test that export_sitemaps method returns valid JSON for sitemaps."""
    exporter = JSONExporter(sitemap_parser_mock)

    expected_output = dumps([
        {"loc": "https://example.com/sitemap1.xml", "lastmod": "2023-01-01T00:00:00+00:00"},
        {"loc": "https://example.com/sitemap2.xml", "lastmod": "2023-01-02T00:00:00+00:00"},
    ])

    result = exporter.export_sitemaps()
    assert result == expected_output


def test_export_urls(sitemap_parser_mock: MagicMock) -> None:
    """Test that export_urls method returns valid JSON for URLs."""
    exporter = JSONExporter(sitemap_parser_mock)

    expected_output = dumps([
        {
            "loc": "https://example.com/page1",
            "lastmod": "2023-01-01T00:00:00+00:00",
            "changefreq": "daily",
            "priority": 1.0,
        },
        {
            "loc": "https://example.com/page2",
            "lastmod": "2023-01-02T00:00:00+00:00",
            "changefreq": "weekly",
            "priority": 0.8,
        },
    ])

    result = exporter.export_urls()
    assert result == expected_output
