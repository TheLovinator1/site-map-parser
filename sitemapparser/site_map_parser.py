import logging

from .data_helpers import data_to_element, download_uri_data
from .sitemap_index import SitemapIndex
from .url_set import UrlSet


class SiteMapParser:
    def __init__(self, uri):
        """Parses and creates sitemap or url instances for the data retrieved

        :param uri: String, uri of the sitemap.xml you want analysed
        """
        self.logger = logging.getLogger(__name__)

        data = download_uri_data(uri)
        root_element = data_to_element(data)

        self.is_sitemap_index = self._is_sitemap_index_element(root_element)

        if self.is_sitemap_index:
            self.logger.info("Root element is sitemap index")
            self._sitemaps = SitemapIndex(root_element)
        else:
            self.logger.info("Root element is url set")
            self._url_set = UrlSet(root_element)

    @staticmethod
    def _is_sitemap_index_element(element):
        return bool(len(element.xpath("/*[local-name()='sitemapindex']")))

    @staticmethod
    def _is_url_set_element(element):
        return bool(len(element.xpath("/*[local-name()='urlset']")))

    def get_sitemaps(self):
        """Retrieve the sitemaps. Can check if 'has_sitemaps()' returns True to
        determine if this should be used without calling it

        :return: iter(Sitemap)
        """
        if not self.has_sitemaps():
            error_msg = "Method called when root is not a <sitemapindex>"
            self.logger.critical(error_msg)
            raise KeyError(error_msg)
        return self._sitemaps

    def get_urls(self):
        """Retrieve the urls. Can check if 'has_urls()' returns True to determine
        if this should be used without actually calling it.

        :return: iter(Url)
        """
        if not self.has_urls():
            error_msg = "Method called when root is not a <urlset>"
            self.logger.critical(error_msg)
            raise KeyError(error_msg)
        return self._url_set

    def has_sitemaps(self):
        """Determine if the URL's data contained sitemaps

        :return: Boolean
        """
        return self.is_sitemap_index

    def has_urls(self):
        """Determine if the URL's data contained urls

        :return: Boolean
        """
        return not self.is_sitemap_index
