import pytest
import requests_mock

from sitemapparser.data_helpers import data_to_element, download_uri_data


def test_download_uri_data_sitemap_index():
    with requests_mock.mock() as m:
        smi_data = open("tests/sitemap_index_data.xml", "rb").read()
        m.get("http://www.example.com/sitemapindex.xml", content=smi_data)
        downloaded_data = download_uri_data("http://www.example.com/sitemapindex.xml")
        assert downloaded_data == smi_data


def test_download_uri_data_urlset():
    with requests_mock.mock() as m:
        us_data = open("tests/urlset_a.xml", "rb").read()
        m.get("http://www.example.com/urlset_a.xml", content=us_data)
        downloaded_data = download_uri_data("http://www.example.com/urlset_a.xml")
        assert downloaded_data == us_data


def test_data_to_element_sitemap_index():
    smi_data = open("tests/sitemap_index_data.xml", "rb").read()
    root_element = data_to_element(smi_data)
    assert len(root_element.xpath("/*[local-name()='sitemapindex']")) == 1
    assert len(root_element.xpath("/*[local-name()='urlset']")) == 0


def test_data_to_element_sitemap_index_broken():
    smi_data = open("tests/sitemap_index_data_broken.xml", "rb").read()
    with pytest.raises(SyntaxError):
        root_element = data_to_element(smi_data)
    # assert len(root_element.xpath("/*[local-name()='sitemapindex']")) == 1
    # assert len(root_element.xpath("/*[local-name()='urlset']")) == 0


def test_data_to_element_urlset():
    us_data = open("tests/urlset_a.xml", "rb").read()
    root_element = data_to_element(us_data)
    assert len(root_element.xpath("/*[local-name()='sitemapindex']")) == 0
    assert len(root_element.xpath("/*[local-name()='urlset']")) == 1
