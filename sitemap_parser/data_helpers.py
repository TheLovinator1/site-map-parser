from __future__ import annotations

from io import BytesIO
from typing import TYPE_CHECKING

import httpx
from loguru import logger
from lxml import etree

if TYPE_CHECKING:
    from xml.etree.ElementTree import Element


def log_request(request: httpx.Request) -> None:
    """Log the request.

    Args:
        request: The request to log
    """
    logger.debug(
        f"Request event hook: {request.method} {request.url} - Waiting for response",
    )


def log_response(response: httpx.Response) -> None:
    """Log the response.

    Args:
        response: The response to log
    """
    request: httpx.Request = response.request
    logger.debug(
        f"Response event hook: {request.method} {request.url} - Status {response.status_code}",  # noqa: E501
    )


def download_uri_data(uri: str) -> bytes:
    """Download the data from the uri.

    Args:
        uri: The uri to download

    Returns:
        The data from the uri
    """
    with httpx.Client(
        timeout=10,
        http2=True,
        follow_redirects=True,
        event_hooks={"request": [log_request], "response": [log_response]},
    ) as client:
        r: httpx.Response = client.get(uri)

    r.raise_for_status()
    logger.debug(f"Request content: {r.content}")
    return r.content


def data_to_element(data: bytes) -> Element:
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
