from datetime import datetime
from io import BytesIO
from unittest.mock import MagicMock

import pytest
from lxml import etree

from sitemapparser.url import Url
from sitemapparser.url_set import UrlSet


class TestUrlSet:
    def setup(self):
        url_set_data_bytes = open("tests/urlset_a.xml", "rb").read()
        utf8_parser = etree.XMLParser(encoding="utf-8")
        self.url_set_data_xml = etree.parse(
            BytesIO(url_set_data_bytes), parser=utf8_parser
        )
        self.url_set_element = self.url_set_data_xml.getroot()
        self.url_element_1 = self.url_set_data_xml.getroot()[0]
        self.url_element_2 = self.url_set_data_xml.getroot()[1]

        # custom element handling
        custom_ele_file = "tests/urlset_a_custom_element.xml"
        url_set_custom_ele_bytes = open(custom_ele_file, "rb").read()
        self.url_set_data_custom_xml = etree.parse(
            BytesIO(url_set_custom_ele_bytes), parser=utf8_parser
        )
        self.url_set_custom_element = self.url_set_data_custom_xml.getroot()
        self.url_element_3 = self.url_set_data_custom_xml.getroot()[0]

    def test_allowed_fields(self):
        for f in UrlSet.allowed_fields:
            assert f in ["loc", "lastmod", "changefreq", "priority"]

    def test_url_from_url_element(self):
        url = UrlSet.url_from_url_element(self.url_element_1)
        assert isinstance(url, Url)
        assert url.loc == "http://www.example.com/page/a/1"
        assert type(url.lastmod) is datetime
        assert str(url.lastmod) == "2005-01-01 00:00:00"
        assert url.changefreq == "monthly"
        assert url.priority == 0.8

    def test_url_from_custom_url_element(self):
        url = UrlSet.url_from_url_element(self.url_element_3)
        assert isinstance(url, Url)
        assert url.loc == "http://www.example.com/page/a/4"
        assert type(url.lastmod) is datetime
        assert str(url.lastmod) == "2006-05-05 00:00:00"
        assert url.changefreq == "monthly"
        assert url.priority == 0.3

    def test_urls_from_url_set_element(self):
        urls = UrlSet.urls_from_url_set_element(self.url_set_element)
        assert len(list(urls)) == 3

    def test_urls_from_url_set_custom_element(self):
        urls = UrlSet.urls_from_url_set_element(self.url_set_custom_element)
        assert len(list(urls)) == 1

    def test_init(self):
        u = UrlSet(self.url_set_element)
        assert len(list(u)) == 3
