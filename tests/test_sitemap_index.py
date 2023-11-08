from __future__ import annotations

from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any

from lxml import etree

from sitemapparser.sitemap import Sitemap
from sitemapparser.sitemap_index import SitemapIndex

if TYPE_CHECKING:
    from collections.abc import Generator


class TestSitemapIndex:
    """Test the SitemapIndex class."""

    def setup(self: TestSitemapIndex) -> None:
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
        sm: Sitemap = SitemapIndex.sitemap_from_sitemap_element(
            self.sitemap_index_element_xml,
        )
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
        si: Generator[
            Sitemap,
            Any,
            None,
        ] = SitemapIndex.sitemaps_from_sitemap_index_element(
            self.sitemap_index_xml_root,
        )
        assert len(list(si)) == amount_of_sitemaps

    def test_init(self: TestSitemapIndex) -> None:
        """Test init.

        Args:
            self: TestSitemapIndex
        """
        amount_of_sitemaps: int = len(self.sitemap_index_xml_root)
        smi = SitemapIndex(self.sitemap_index_xml_root)
        assert len(list(smi)) == amount_of_sitemaps
