from io import BytesIO

import pytest
import requests_mock
from lxml import etree

from sitemapparser.site_map_parser import SiteMapParser


class TestSiteMapper:
    def setup(self):
        sitemap_index_data = open("tests/sitemap_index_data.xml", "rb").read()
        utf8_parser = etree.XMLParser(encoding="utf-8")
        self.sitemap_index_xml_root = etree.parse(
            BytesIO(sitemap_index_data),
            parser=utf8_parser,
        ).getroot()
        self.sitemap_index_element_xml = self.sitemap_index_xml_root[0]

        url_set_data_bytes = open("tests/urlset_a.xml", "rb").read()
        utf8_parser = etree.XMLParser(encoding="utf-8")
        self.url_set_data_xml = etree.parse(
            BytesIO(url_set_data_bytes),
            parser=utf8_parser,
        )
        self.url_set_element = self.url_set_data_xml.getroot()
        self.url_element_1 = self.url_set_data_xml.getroot()[0]

    def test_is_sitemap_index_element(self):
        sitemap_index_result = SiteMapParser._is_sitemap_index_element(
            self.sitemap_index_xml_root,
        )
        url_set_result = SiteMapParser._is_sitemap_index_element(self.url_set_element)
        assert sitemap_index_result == True
        assert url_set_result == False

    def test_is_url_set_element(self):
        url_set_result = SiteMapParser._is_url_set_element(self.url_set_element)
        sitemap_index_result = SiteMapParser._is_url_set_element(
            self.sitemap_index_xml_root,
        )
        assert url_set_result == True
        assert sitemap_index_result == False

    def test_get_sitemaps(self):
        with requests_mock.mock() as m:
            smi_data = open("tests/sitemap_index_data.xml", "rb").read()
            m.get("http://www.sitemap-example.com", content=smi_data)
            sm = SiteMapParser("http://www.sitemap-example.com")
            site_maps = sm.get_sitemaps()
            assert len(list(site_maps)) == 2

    def test_get_sitemaps_inappropriate_call(self):
        with requests_mock.mock() as m:
            us_data = open("tests/urlset_a.xml", "rb").read()
            m.get("http://www.url-example.com", content=us_data)
            sm = SiteMapParser("http://www.url-example.com")
            with pytest.raises(KeyError):
                site_maps = sm.get_sitemaps()

    def test_get_urls(self):
        with requests_mock.mock() as m:
            us_data = open("tests/urlset_a.xml", "rb").read()
            m.get("http://www.url-example.com", content=us_data)
            sm = SiteMapParser("http://www.url-example.com")
            url_set = sm.get_urls()
            assert len(list(url_set)) == 3

    def test_get_urls_inappropriate_call(self):
        with requests_mock.mock() as m:
            smi_data = open("tests/sitemap_index_data.xml", "rb").read()
            m.get("http://www.sitemap-example.com", content=smi_data)
            smi = SiteMapParser("http://www.sitemap-example.com")
            with pytest.raises(KeyError):
                url_set = smi.get_urls()

    def test_has_sitemaps(self):
        with requests_mock.mock() as m:
            smi_data = open("tests/sitemap_index_data.xml", "rb").read()
            m.get("http://www.sitemap-example.com", content=smi_data)
            sm = SiteMapParser("http://www.sitemap-example.com")
            assert sm.has_sitemaps() is True
            assert sm.has_urls() is False

    def test_has_urls(self):
        with requests_mock.mock() as m:
            us_data = open("tests/urlset_a.xml", "rb").read()
            m.get("http://www.url-example.com", content=us_data)
            sm = SiteMapParser("http://www.url-example.com")
            assert sm.has_urls() is True
            assert sm.has_sitemaps() is False

    def test_get_urls_multiple_iters(self):
        with requests_mock.mock() as m:
            us_data = open("tests/urlset_a.xml", "rb").read()
            m.get("http://www.url-example.com", content=us_data)
            sm = SiteMapParser("http://www.url-example.com")
            urls_1 = iter(sm.get_urls())
            urls_2 = iter(sm.get_urls())
            assert str(next(urls_1)) == "http://www.example.com/page/a/1"
            assert str(next(urls_2)) == "http://www.example.com/page/a/1"
            assert str(next(urls_1)) == "http://www.example.com/page/a/2"
            assert str(next(urls_1)) == "http://www.example.com/page/a/3"

    def test_get_sitemaps_multiple_iters(self):
        with requests_mock.mock() as m:
            us_data = open("tests/sitemap_index_data.xml", "rb").read()
            m.get("http://www.url-example.com", content=us_data)
            sm = SiteMapParser("http://www.url-example.com")
            sm_1 = iter(sm.get_sitemaps())
            sm_2 = iter(sm.get_sitemaps())

            assert str(next(sm_1)) == "http://www.example.com/sitemap_a.xml"
            assert str(next(sm_1)) == "https://www.example.com/sitemap_b.xml"
            assert str(next(sm_2)) == "http://www.example.com/sitemap_a.xml"
