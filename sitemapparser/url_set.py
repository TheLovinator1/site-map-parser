import logging

from .url import Url


class UrlSet:
    allowed_fields = ["loc", "lastmod", "changefreq", "priority"]

    def __init__(self, urlset_element):
        self.urlset_element = urlset_element

    @staticmethod
    def url_from_url_element(url_element):
        logger = logging.getLogger(__name__)
        logger.debug(f"urls_from_url_element {url_element}")
        url_data = {}
        for ele in url_element:
            name = ele.xpath("local-name()")
            if name in UrlSet.allowed_fields:
                url_data[name] = ele.xpath("text()")[0]

        logger.debug(f"url_data {url_data}")
        return Url(**url_data)

    @staticmethod
    def urls_from_url_set_element(url_set_element):
        logger = logging.getLogger(__name__)
        logger.debug(f"urls_from_url_set_element {url_set_element}")

        for url_element in url_set_element:
            yield UrlSet.url_from_url_element(url_element)

    def __iter__(self):
        return UrlSet.urls_from_url_set_element(self.urlset_element)
