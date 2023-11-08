import logging
from io import BytesIO

import requests
from lxml import etree

# use Bytes throughout because that's how lxml says XML should be used


def download_uri_data(uri):
    """
    returns file object
    """
    logger = logging.getLogger(__name__)
    logger.info("Requesting data from: {}".format(uri))
    # using requests to follow any redirects that happen
    headers = {"Content-Type": "application/xml;charset=utf-8"}
    r = requests.get(uri, headers=headers)
    # ensure it's the decompressed content
    r.raw.decode_content = True
    logger.debug("Request content: {}".format(r.content))
    return r.content


def data_to_element(data):
    """
    data parameter should be bytes
    """
    logger = logging.getLogger(__name__)
    content = BytesIO(data)
    root = None
    try:
        utf8_parser = etree.XMLParser(encoding="utf-8")
        downloaded_xml = etree.parse(content, parser=utf8_parser)
        logger.debug("Downloaded: {}".format(downloaded_xml))
        root = downloaded_xml.getroot()
        logger.debug("Downloaded root {}".format(root))
    except SyntaxError as err:
        logger.warning("Parsing failed {}".format(err))
        raise err
    return root
