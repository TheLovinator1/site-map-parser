from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from xml.etree.ElementTree import Element

from loguru import logger

from .data_helpers import bytes_to_element, download_uri_data
from .sitemap_index import SitemapIndex
from .url_set import UrlSet

if TYPE_CHECKING:
    from xml.etree.ElementTree import Element


@dataclass(slots=True)
class SiteMapParser:
    """Parses a sitemap or sitemap index and returns the appropriate object."""

    uri: str
    is_sitemap_index: bool = field(init=False)
    _sitemaps: SitemapIndex | None = field(init=False, default=None)
    _url_set: UrlSet | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        """Post-initialization processing."""
        data = download_uri_data(self.uri)
        root_element = bytes_to_element(data)

        self.is_sitemap_index = self._is_sitemap_index_element(root_element)

        if self.is_sitemap_index:
            logger.info("Root element is sitemap index")
            self._sitemaps = SitemapIndex(index_element=root_element)
        else:
            logger.info("Root element is url set")
            self._url_set = UrlSet(urlset_element=root_element)

    @staticmethod
    def _is_sitemap_index_element(element: Element) -> bool:
        """Determine if the element is a sitemapindex.

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

    def get_sitemaps(self) -> SitemapIndex:
        """Retrieve the sitemaps.

        Can check if 'has_sitemaps()' returns True to determine
        if this should be used without calling it

        Args:
            self: The SiteMapParser instance

        Raises:
            KeyError: If the root is not a <sitemapindex>

        Returns:
            SitemapIndex
        """
        if not self.has_sitemaps():
            error_msg = "Method called when root is not a <sitemapindex>"
            logger.critical(error_msg)
            raise KeyError(error_msg)

        if self._sitemaps is None:
            msg = "Sitemaps are not available"
            raise KeyError(msg)

        return self._sitemaps

    def get_urls(self) -> UrlSet:
        """Retrieve the urls.

        Args:
            self: The SiteMapParser instance

        Raises:
            KeyError: If the root is not a <urlset>

        Returns:
            UrlSet
        """
        if not self.has_urls():
            error_msg = "Method called when root is not a <urlset>"
            logger.critical(error_msg)
            raise KeyError(error_msg)

        if self._url_set is None:
            msg = "URLs are not available"
            raise KeyError(msg)

        return self._url_set

    def has_sitemaps(self) -> bool:
        """Determine if the URL's data contained sitemaps.

        A sitemap can contain other sitemaps. For example: <https://www.webhallen.com/sitemap.xml>

        Args:
            self: The SiteMapParser instance

        Returns:
            Boolean
        """
        return self.is_sitemap_index

    def has_urls(self) -> bool:
        """Determine if the URL's data contained urls.

        Args:
            self: The SiteMapParser instance

        Returns:
            Boolean
        """
        return not self.is_sitemap_index

    def __str__(self) -> str:
        """String representation of the SiteMapParser instance.

        Args:
            self: The SiteMapParser instance

        Returns:
            str
        """
        return str(self._sitemaps if self.has_sitemaps() else self._url_set)
