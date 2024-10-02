from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING
from xml.etree.ElementTree import Element

import httpx
from loguru import logger
from lxml import etree

if TYPE_CHECKING:
    from xml.etree.ElementTree import Element


def download_uri_data(uri: str) -> bytes:
    """Download the data from the uri.

    Args:
        uri: The uri to download. Expected format: HTTP/HTTPS URL.

    Returns:
        The data from the uri
    """
    with httpx.Client(timeout=10, http2=True, follow_redirects=True) as client:
        r: httpx.Response = client.get(uri)

    r.raise_for_status()
    logger.debug("Downloaded data from {}", uri)

    max_log_length = 100
    truncated_content = r.content[:max_log_length] + b"..." if len(r.content) > max_log_length else r.content
    logger.debug("Downloaded data: {}", truncated_content)

    return r.content


def bytes_to_element(data: bytes) -> Element:
    """Convert the data to an lxml element.

    Args:
        data: The data to convert

    Raises:
        etree.XMLSyntaxError: Syntax error while parsing an XML document

    Returns:
        The lxml element as an Element from lxml.etree
    """
    content = BytesIO(data)
    try:
        utf8_parser = etree.XMLParser(encoding="utf-8")
        downloaded_xml = etree.parse(content, parser=utf8_parser)
        logger.debug(f"Parsed XML: {downloaded_xml}")
        root = downloaded_xml.getroot()

    except etree.XMLSyntaxError as err:
        logger.error(f"Error parsing XML: {err}")
        raise

    logger.debug(f"Parsed XML root element: {root}")
    return root
