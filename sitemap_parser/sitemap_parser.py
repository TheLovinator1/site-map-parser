from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from .data_helpers import data_to_element, download_uri_data
from .sitemap_index import SitemapIndex
from .url_set import UrlSet

if TYPE_CHECKING:
    from xml.etree.ElementTree import Element


class SiteMapParser:
    """Parses a sitemap or sitemap index and returns the appropriate object."""

    def __init__(self: SiteMapParser, uri: str) -> None:
        """Creates a SiteMapParser instance.

        Args:
            uri: The uri to parse
        """
        data: bytes = download_uri_data(uri)
        root_element: Element = data_to_element(data)

        self.is_sitemap_index: bool = self._is_sitemap_index_element(root_element)

        if self.is_sitemap_index:
            logger.info("Root element is sitemap index")
            self._sitemaps = SitemapIndex(root_element)
        else:
            logger.info("Root element is url set")
            self._url_set = UrlSet(root_element)

    @staticmethod
    def _is_sitemap_index_element(element: Element) -> bool:
        """Determine if the element is a <sitemapindex>.

        Args:
            element: The element to check

        Returns:
            Boolean
        """
        return bool(len(element.xpath("/*[local-name()='sitemapindex']")))  # type: ignore[attr-defined]

    @staticmethod
    def _is_url_set_element(element: Element) -> bool:
        """Determine if the element is a <urlset>.

        Args:
            element: The element to check

        Returns:
            Boolean
        """
        return bool(len(element.xpath("/*[local-name()='urlset']")))  # type: ignore[attr-defined]

    def get_sitemaps(self: SiteMapParser) -> SitemapIndex:
        """Retrieve the sitemaps.

        Can check if 'has_sitemaps()' returns True to determine
        if this should be used without calling it

        Args:
            self: The SiteMapParser instance

        Raises:
            KeyError: If the root is not a <sitemapindex>

        Returns:
            iter(Sitemap)
        """
        if not self.has_sitemaps():
            error_msg = "Method called when root is not a <sitemapindex>"
            logger.critical(error_msg)
            raise KeyError(error_msg)
        return self._sitemaps

    def get_urls(self: SiteMapParser) -> UrlSet:
        """Retrieve the urls.

        Args:
            self: The SiteMapParser instance

        Raises:
            KeyError: If the root is not a <urlset>

        Returns:
            iter(Url)
        """
        if not self.has_urls():
            error_msg = "Method called when root is not a <urlset>"
            logger.critical(error_msg)
            raise KeyError(error_msg)
        return self._url_set

    def has_sitemaps(self: SiteMapParser) -> bool:
        """Determine if the URL's data contained sitemaps.

        A sitemap can contain other sitemaps. For example: <https://www.webhallen.com/sitemap.xml>

        Args:
            self: The SiteMapParser instance

        Returns:
            Boolean
        """
        return self.is_sitemap_index

    def has_urls(self: SiteMapParser) -> bool:
        """Determine if the URL's data contained urls.

        Args:
            self: The SiteMapParser instance

        Returns:
            Boolean
        """
        return not self.is_sitemap_index

    def __str__(self: SiteMapParser) -> str:
        """String representation of the SiteMapParser instance.

        Args:
            self: The SiteMapParser instance

        Returns:
            String
        """
        if self.has_sitemaps():
            return str(self._sitemaps)
        return str(self._url_set)
