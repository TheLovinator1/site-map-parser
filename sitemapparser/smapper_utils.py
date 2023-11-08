import argparse
import logging
import os
from inspect import getmembers, isclass

from . import exporters


def get_logging_config():
    log_config = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "logging_config.ini",
    )
    log_file = os.path.join(os.path.expanduser("~"), "sitemap_run.log")
    return log_config, log_file


def get_exporters():
    return {m[1].short_name: m[1] for m in getmembers(exporters, isclass)}


def uri_modifier(url):
    if not url.startswith("https://") and not url.startswith("http://"):
        url = "http://" + url

    if not url.endswith(".xml"):
        if not url.endswith("/"):
            url = url + "/"
        url = url + "sitemap.xml"
    return url


def get_args(sys_argv):
    """:return: (url, log)"""
    logger = logging.getLogger(__name__)
    exporter_choices = get_exporters().keys()
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("url", help="Url & path to sitemap.xml")
    arg_parser.add_argument(
        "--log",
        "-l",
        default="INFO",
        choices=[
            "CRITICAL",
            "ERROR",
            "WARNING",
            "INFO",
            "DEBUG",
        ],
    )
    arg_parser.add_argument(
        "--exporter",
        "-e",
        help="Choose which exporter is to be used, defaults to CSV",
        default="csv",
        choices=exporter_choices,
    )

    logger.debug(f"sys_argv: {sys_argv}")
    found_args = arg_parser.parse_args(sys_argv)
    logger.debug(f"Found arguments: {found_args}")

    return (found_args.url, found_args.log, found_args.exporter)
