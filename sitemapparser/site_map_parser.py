from __future__ import annotations

import logging

from .data_helpers import data_to_element, download_uri_data
from .sitemap_index import SitemapIndex
from .url_set import UrlSet


class SiteMapParser:
    """Parses a sitemap or sitemap index and returns the appropriate object."""

    def __init__(self: SiteMapParser, uri: str) -> None:
        """Creates a SiteMapParser instance.

        Args:
            uri: The uri to parse
        """
        self.logger: logging.Logger = logging.getLogger(__name__)

        data: bytes = download_uri_data(uri)
        root_element = data_to_element(data)

        self.is_sitemap_index: bool = self._is_sitemap_index_element(root_element)

        if self.is_sitemap_index:
            self.logger.info("Root element is sitemap index")
            self._sitemaps = SitemapIndex(root_element)
        else:
            self.logger.info("Root element is url set")
            self._url_set = UrlSet(root_element)

    @staticmethod
    def _is_sitemap_index_element(element) -> bool:  # noqa: ANN001
        """Determine if the element is a <sitemapindex>.

        Args:
            element: The element to check

        Returns:
            Boolean
        """
        return bool(len(element.xpath("/*[local-name()='sitemapindex']")))

    @staticmethod
    def _is_url_set_element(element) -> bool:  # noqa: ANN001
        """Determine if the element is a <urlset>.

        Args:
            element: The element to check

        Returns:
            Boolean
        """
        return bool(len(element.xpath("/*[local-name()='urlset']")))

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
            self.logger.critical(error_msg)
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
            self.logger.critical(error_msg)
            raise KeyError(error_msg)
        return self._url_set

    def has_sitemaps(self: SiteMapParser) -> bool:
        """Determine if the URL's data contained sitemaps.

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
