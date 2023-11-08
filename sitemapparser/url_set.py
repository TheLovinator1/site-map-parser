from __future__ import annotations

import logging
import typing

from .url import Url


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

    def __init__(self: UrlSet, urlset_element) -> None:  # noqa: ANN001
        """Creates a UrlSet instance.

        Args:
            urlset_element: lxml representation of a <urlset> element
        """
        self.urlset_element = urlset_element

    @staticmethod
    def url_from_url_element(url_element) -> Url:  # noqa: ANN001
        """Creates a Url instance from a <url> element.

        Args:
            url_element: lxml representation of a <url> element

        Returns:
            Url instance
        """
        logger: logging.Logger = logging.getLogger(__name__)
        logger.debug(f"urls_from_url_element {url_element}")
        url_data: dict = {}
        for ele in url_element:
            name = ele.xpath("local-name()")
            if name in UrlSet.allowed_fields:
                url_data[name] = ele.xpath("text()")[0]

        logger.debug(f"url_data {url_data}")
        return Url(**url_data)

    @staticmethod
    def urls_from_url_set_element(
        url_set_element,  # noqa: ANN001
    ) -> typing.Generator[Url, typing.Any, None]:
        """Generator for Url instances from a <urlset> element.

        Args:
            url_set_element: lxml representation of a <urlset> element

        Returns:
            Generator[Url, Any, None]

        Yields:
            Url instances
        """
        logger: logging.Logger = logging.getLogger(__name__)
        logger.debug(f"urls_from_url_set_element {url_set_element}")

        for url_element in url_set_element:
            yield UrlSet.url_from_url_element(url_element)

    def __iter__(self: UrlSet) -> typing.Generator[Url, typing.Any, None]:
        """Generator for Url instances from a <urlset> element.

        Args:
            self: The UrlSet instance

        Returns:
            Generator[Url, Any, None]
        """
        return UrlSet.urls_from_url_set_element(self.urlset_element)
