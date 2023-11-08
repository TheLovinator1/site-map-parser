import argparse
import os
from unittest.mock import MagicMock

from sitemapparser.smapper_utils import (
    get_args,
    get_exporters,
    get_logging_config,
    uri_modifier,
)


def test_get_logging_config(monkeypatch):
    def mock_expanduser(value):
        return "/home/test"

    monkeypatch.setattr(os.path, "expanduser", mock_expanduser)
    logging_config, log_file = get_logging_config()

    assert os.path.exists(logging_config)
    assert log_file == "/home/test/sitemap_run.log"


def test_get_exporters():
    exporters = get_exporters()
    assert len(exporters) == 2
    assert "csv" in exporters
    assert "json" in exporters
    assert "fake" not in exporters


def test_uri_modifier_begins():
    test_url1 = "example.com"
    assert uri_modifier(test_url1) == "http://example.com/sitemap.xml"
    test_url2 = "http://www.example.com"
    assert uri_modifier(test_url2) == "http://www.example.com/sitemap.xml"


def test_uri_modifier_ends():
    test_url1 = "http://www.example.com"
    assert uri_modifier(test_url1) == "http://www.example.com/sitemap.xml"
    test_url2 = "http://www.example.com/"
    assert uri_modifier(test_url2) == "http://www.example.com/sitemap.xml"
    test_url3 = "http://www.example.com/sitemap.xml"
    assert uri_modifier(test_url3) == "http://www.example.com/sitemap.xml"


def test_get_args_long():
    sys_argv = ["http://www.example.com", "--log", "DEBUG", "--exporter", "json"]
    (url, logging_level, exporter_format) = get_args(sys_argv)
    assert url == "http://www.example.com"
    assert logging_level == "DEBUG"
    assert exporter_format == "json"


def test_get_args_default():
    sys_argv = [
        "http://www.example.com",
    ]
    (url, logging_level, exporter_format) = get_args(sys_argv)
    assert url == "http://www.example.com"
    assert logging_level == "INFO"
    assert exporter_format == "csv"
