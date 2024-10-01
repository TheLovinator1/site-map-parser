from __future__ import annotations

import typing

from loguru import logger

from .url import Url

if typing.TYPE_CHECKING:
    from xml.etree.ElementTree import Element


class UrlSet:
    """Class to represent a <urlset> element.

    Returns:
        UrlSet instance

    Yields:
        Url instances
    """

    allowed_fields: typing.ClassVar[list[str]] = [
        "loc",
        "lastmod",
        "changefreq",
        "priority",
    ]

    def __init__(self: UrlSet, urlset_element: Element) -> None:
        """Creates a UrlSet instance.

        Args:
            urlset_element: lxml representation of a <urlset> element
        """
        self.urlset_element: Element = urlset_element

    @staticmethod
    def url_from_url_element(url_element: Element) -> Url:
        """Creates a Url instance from a <url> element.

        Args:
            url_element: lxml representation of a <url> element

        Returns:
            Url instance
        """
        logger.debug(f"urls_from_url_element {url_element}")
        url_data: dict = {}
        for ele in url_element:
            name = ele.xpath("local-name()")  # type: ignore[attr-defined]
            if name in UrlSet.allowed_fields:
                url_data[name] = ele.xpath("text()")[0]  # type: ignore[attr-defined]

        logger.debug(f"url_data {url_data}")
        return Url(**url_data)

    @staticmethod
    def urls_from_url_set_element(
        url_set_element: Element,
    ) -> typing.Generator[Url, typing.Any, None]:
        """Generator for Url instances from a <urlset> element.

        Args:
            url_set_element: lxml representation of a <urlset> element

        Returns:
            Generator[Url, Any, None]

        Yields:
            Url instances
        """
        logger.debug(f"urls_from_url_set_element {url_set_element}")

        for url_element in url_set_element:
            yield UrlSet.url_from_url_element(url_element)

    def __iter__(self: UrlSet) -> typing.Iterator[Url]:
        """Generator for Url instances from a <urlset> element.

        Args:
            self: The UrlSet instance

        Returns:
            Generator[Url, Any, None]
        """
        return UrlSet.urls_from_url_set_element(self.urlset_element)
