import logging
from io import BytesIO

import requests
from lxml import etree

# use Bytes throughout because that's how lxml says XML should be used


def download_uri_data(uri):
    """Returns file object"""
    logger = logging.getLogger(__name__)
    logger.info(f"Requesting data from: {uri}")
    # using requests to follow any redirects that happen
    headers = {"Content-Type": "application/xml;charset=utf-8"}
    r = requests.get(uri, headers=headers)
    # ensure it's the decompressed content
    r.raw.decode_content = True
    logger.debug(f"Request content: {r.content}")
    return r.content


def data_to_element(data):
    """Data parameter should be bytes"""
    logger = logging.getLogger(__name__)
    content = BytesIO(data)
    root = None
    try:
        utf8_parser = etree.XMLParser(encoding="utf-8")
        downloaded_xml = etree.parse(content, parser=utf8_parser)
        logger.debug(f"Downloaded: {downloaded_xml}")
        root = downloaded_xml.getroot()
        logger.debug(f"Downloaded root {root}")
    except SyntaxError as err:
        logger.warning(f"Parsing failed {err}")
        raise err
    return root
