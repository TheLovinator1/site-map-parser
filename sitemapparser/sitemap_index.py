from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from sitemapparser.sitemap import Sitemap

if TYPE_CHECKING:
    from collections.abc import Generator


class SitemapIndex:
    """Represents a <sitemapindex> element."""

    def __init__(self: SitemapIndex, index_element) -> None:  # noqa: ANN001
        """Creates a SitemapIndex instance.

        Args:
            self: The SitemapIndex instance
            index_element: lxml representation of a <sitemapindex> element
        """
        self.index_element = index_element

    @staticmethod
    def sitemap_from_sitemap_element(sitemap_element) -> Sitemap:  # noqa: ANN001
        """Creates a Sitemap instance from a <sitemap> element.

        Args:
            sitemap_element: lxml representation of a <sitemap> element

        Returns:
            Sitemap instance
        """
        logger: logging.Logger = logging.getLogger(__name__)
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
        index_element,  # noqa: ANN001
    ) -> Generator[Sitemap, Any, None]:
        """Generator for Sitemap instances from a <sitemapindex> element.

        Args:
            index_element: lxml representation of a <sitemapindex> element

        Yields:
            Sitemap instance
        """
        logger: logging.Logger = logging.getLogger(__name__)
        msg = "Generating sitemaps from {}"
        logger.debug(msg.format(index_element))

        # handle child elements, <sitemap>
        sitemaps = index_element.findall("./*")
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
