from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from sitemap_parser.data_helpers import bytes_to_element, download_uri_data

if TYPE_CHECKING:
    from xml.etree.ElementTree import Element

    from pytest_httpx import HTTPXMock


def test_download_uri_data_sitemap_index(httpx_mock: HTTPXMock) -> None:
    """Test download_uri_data() with a sitemap index."""
    smi_data: bytes = Path.open(Path("tests/sitemap_index_data.xml"), "rb").read()
    httpx_mock.add_response(
        url="http://www.example.com/sitemapindex.xml",
        content=smi_data,
    )
    downloaded_data: bytes = download_uri_data(
        "http://www.example.com/sitemapindex.xml",
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
        "http://www.example.com/urlset_a.xml",
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
