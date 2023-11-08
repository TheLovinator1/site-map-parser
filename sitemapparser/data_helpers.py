from __future__ import annotations

from io import BytesIO

import requests
from loguru import logger
from lxml import etree


def download_uri_data(uri: str) -> bytes:
    """Download the data from the uri.

    Args:
        uri: The uri to download

    Returns:
        The data from the uri
    """
    logger.info(f"Requesting data from: {uri}")

    # using requests to follow any redirects that happen
    headers: dict[str, str] = {"Content-Type": "application/xml;charset=utf-8"}
    r: requests.Response = requests.get(uri, headers=headers, timeout=10)

    # ensure it's the decompressed content
    r.raw.decode_content = True
    logger.debug(f"Request content: {r.content}")
    return r.content


def data_to_element(data: bytes):  # noqa: ANN201
    """Convert the data to an lxml element.

    Args:
        data: The data to convert

    Returns:
        The lxml element
    """
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
        raise
    return root
