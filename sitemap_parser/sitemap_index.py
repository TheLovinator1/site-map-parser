from __future__ import annotations

from typing import TYPE_CHECKING, Any

from loguru import logger

from sitemap_parser.sitemap import Sitemap

if TYPE_CHECKING:
    from collections.abc import Generator
    from xml.etree.ElementTree import Element

# Element doesn't have xpath method
# pyright: reportGeneralTypeIssues=false


class SitemapIndex:
    """Represents a <sitemapindex> element."""

    def __init__(self: SitemapIndex, index_element: Element) -> None:
        """Creates a SitemapIndex instance.

        Args:
            self: The SitemapIndex instance
            index_element: lxml representation of a <sitemapindex> element
        """
        self.index_element: Element = index_element

    @staticmethod
    def sitemap_from_sitemap_element(sitemap_element: Element) -> Sitemap:
        """Creates a Sitemap instance from a <sitemap> element.

        Args:
            sitemap_element: lxml representation of a <sitemap> element

        Returns:
            Sitemap instance
        """
        sitemap_data: dict = {}
        for ele in sitemap_element:
            name = ele.xpath("local-name()")
            value = ele.xpath("text()")[0]
            sitemap_data[name] = value

        msg = "Returning sitemap object with data: {}"
        logger.debug(msg.format(sitemap_data))
        return Sitemap(**sitemap_data)

    @staticmethod
    def sitemaps_from_sitemap_index_element(
        index_element: Element,
    ) -> Generator[Sitemap, Any, None]:
        """Generator for Sitemap instances from a <sitemapindex> element.

        Args:
            index_element: lxml representation of a <sitemapindex> element

        Yields:
            Sitemap instance
        """
        logger.debug("Generating sitemaps from {}", index_element)

        # handle child elements, <sitemap>
        sitemaps: list[Element] = index_element.findall("./*")
        for sm_element in sitemaps:
            yield SitemapIndex.sitemap_from_sitemap_element(sm_element)

    def __iter__(self: SitemapIndex) -> Generator[Sitemap, Any, None]:
        """Generator for Sitemap instances from a <sitemapindex> element.

        Args:
            self: The SitemapIndex instance

        Returns:
            Sitemap instance

        Yields:
            Sitemap instance
        """
        return SitemapIndex.sitemaps_from_sitemap_index_element(self.index_element)

    def __str__(self: SitemapIndex) -> str:
        """String representation of the SitemapIndex instance.

        Args:
            self: The SitemapIndex instance

        Returns:
            String
        """
        return "SitemapIndex"
