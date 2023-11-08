import logging

from sitemapparser.sitemap import Sitemap


class SitemapIndex:
    def __init__(self, index_element):
        """
        Creates a 'sitemaps' property, an iterator for children of an
        lxml <sitemapindex> representation
        :param index_element: lxml 'sitemapindex' element
        """
        self.index_element = index_element

    @staticmethod
    def sitemap_from_sitemap_element(sitemap_element):
        """
        Creates a Sitemap instance for each sitemap element passed
        :param sitemap_element: lxml representation of a <sitemap> element
        :return: Sitemap instance
        """
        logger = logging.getLogger(__name__)
        sitemap_data = {}
        for ele in sitemap_element:
            name = ele.xpath("local-name()")
            value = ele.xpath("text()")[0]
            sitemap_data[name] = value

        msg = "Returning sitemap object with data: {}"
        logger.debug(msg.format(sitemap_data))
        return Sitemap(**sitemap_data)

    @staticmethod
    def sitemaps_from_sitemap_index_element(index_element):
        """
        Iterator to return the sitemaps from a lxml <sitemapindex> element
        :param index_element: lxml representation of a <sitemapindex> element
        :return: iter(Sitemap) instances
        """
        logger = logging.getLogger(__name__)
        msg = "Generating sitemaps from {}"
        logger.debug(msg.format(index_element))
        # handle child elements, <sitemap>
        sitemaps = index_element.findall("./*")
        for sm_element in sitemaps:
            yield SitemapIndex.sitemap_from_sitemap_element(sm_element)

    def __iter__(self):
        return SitemapIndex.sitemaps_from_sitemap_index_element(self.index_element)
