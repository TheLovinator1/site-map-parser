from __future__ import annotations

import logging
import re
import typing
from datetime import datetime
from io import BytesIO
from json import dumps
from pathlib import Path
from typing import Any, Literal
from xml.etree.ElementTree import Element

import hishel
import httpx
from dateutil import parser
from lxml import etree

if typing.TYPE_CHECKING:
    from collections.abc import Generator, Iterator
    from xml.etree.ElementTree import Element

__all__: list[str] = ["JSONExporter", "SiteMapParser", "Sitemap", "SitemapIndex", "Url", "UrlSet"]

logging.basicConfig(level=logging.DEBUG)
logger: logging.Logger = logging.getLogger("sitemap_parser")

Freqs = Literal["always", "hourly", "daily", "weekly", "monthly", "yearly", "never"]
ValidFreqs = tuple[
    Literal["always"],
    Literal["hourly"],
    Literal["daily"],
    Literal["weekly"],
    Literal["monthly"],
    Literal["yearly"],
    Literal["never"],
]
Fields = tuple[Literal["loc"], Literal["lastmod"], Literal["changefreq"], Literal["priority"]]
UrlFields = tuple[Literal["loc"], Literal["lastmod"], Literal["changefreq"], Literal["priority"]]
SitemapFields = tuple[Literal["loc"], Literal["lastmod"]]


class BaseData:
    """Base class for sitemap data.

    Provides common properties and methods for sitemap and sitemap index entries,
    such as location (`loc`) and last modified time (`lastmod`).
    """

    def __init__(self) -> None:
        self._lastmod: datetime | None = None
        self._loc: str | None = None

    @property
    def lastmod(self) -> datetime | None:
        """Get the last modified datetime.

        Returns:
            datetime | None: The datetime when the resource was last modified, or None if not set.
        """
        return self._lastmod

    @lastmod.setter
    def lastmod(self, value: str | None) -> None:
        """Set the last modified datetime.

        Parses an ISO-8601 datetime string into a datetime object.

        Args:
            value (str | None): An ISO-8601 formatted datetime string, or None.
        """
        self._lastmod = parser.isoparse(value) if value is not None else None

    @property
    def loc(self) -> str | None:
        """Get the location URL.

        Returns:
            str | None: The URL of the resource.
        """
        return self._loc

    @loc.setter
    def loc(self, value: str | None) -> None:
        """Set the location URL.

        Validates that the provided value is a valid URL.

        Args:
            value (str | None): The URL to set.

        Raises:
            ValueError: If the value is not a valid URL.
        """
        # Only allow strings
        if not isinstance(value, str):
            value = str(value)

        # Check if the URL is valid
        if not re.match(r"http[s]?://", value):
            msg: str = f"{value} is not a valid URL"
            raise ValueError(msg)

        # Set the value
        self._loc = value


def download_uri_data(uri: str, *, hishel_client: hishel.CacheClient | None = None, should_cache: bool = True) -> bytes:
    """Download the data from the uri.

    Args:
        uri(str): The uri to download. Expected format: HTTP/HTTPS URL.
        hishel_client(hishel.CacheClient): The Hishel client to use for downloading the data. If None, the data will be downloaded without caching.
        should_cache(bool): Whether to cache the request with Hishel (https://hishel.com/) or not.

    Returns:
        bytes: The data from the uri
    """  # noqa: E501
    if should_cache and hishel_client is not None:
        with hishel_client as client:
            logger.info("Downloading with cache from %s", uri)
            r: httpx.Response = client.get(uri)
    else:
        with httpx.Client(timeout=10, http2=True, follow_redirects=True) as client:
            logger.info("Downloading without cache from %s", uri)
            r: httpx.Response = client.get(uri)

    log_cache_usage(request=r)

    r.raise_for_status()
    logger.debug("Downloaded data from %s", uri)

    max_log_length = 100
    truncated_content: bytes = r.content[:max_log_length] + b"..." if len(r.content) > max_log_length else r.content
    logger.debug("Downloaded data: %s", truncated_content)

    return r.content


def log_cache_usage(request: httpx.Response) -> None:
    """Log if the data was retrieved from cache.

    Args:
        request (httpx.Response): The response object from the download.
    """
    from_cache: Any | bool = request.extensions.get("from_cache", False)
    if from_cache:
        logger.info("%s was retrieved from cache", request.url)


def bytes_to_element(data: bytes) -> Element:
    """Convert the data to an lxml element.

    Args:
        data(bytes): The data to convert

    Raises:
        etree.XMLSyntaxError: Syntax error while parsing an XML document

    Returns:
        Element: The lxml element as an Element from lxml.etree
    """
    content = BytesIO(data)
    try:
        utf8_parser = etree.XMLParser(encoding="utf-8")
        downloaded_xml: etree._ElementTree = etree.parse(content, parser=utf8_parser)  # type: ignore[attr-defined]
        logger.debug("Parsed XML: %s", downloaded_xml)
        root: Element | Any = downloaded_xml.getroot()

    except etree.XMLSyntaxError:
        logger.exception("Error parsing XML")
        raise

    logger.debug("Parsed XML root element: %s", root)
    return root


class Sitemap(BaseData):
    """Representation of the <sitemap> element."""

    fields: tuple[Literal["loc"], Literal["lastmod"]] = "loc", "lastmod"

    def __init__(self, loc: str, lastmod: str | None = None) -> None:
        """Representation of the <sitemap> element.

        Args:
            loc: String, URL of the page.
            lastmod: str | None, The date of last modification of the file.
        """
        self.loc = loc
        self.lastmod = lastmod

    def __str__(self) -> str:
        """String representation of the Sitemap instance.

        Raises:
            ValueError: If loc is None.

        Returns:
            The URL of the page.
        """
        if self.loc is None:
            msg = "loc cannot be None"
            raise ValueError(msg)

        return self.loc

    def __repr__(self) -> str:
        """String representation of the Sitemap instance.

        Returns:
            The URL of the page.
        """
        return f"<Sitemap {self.loc}>"


class Url(BaseData):
    """Representation of the <url> element.

    Args:
        BaseData: Base class for all data classes

    Raises:
        ValueError: If `changefreq` is not an allowed value.
        ValueError: If `priority` is not between 0.0 and 1.0.
    """

    fields: Fields = ("loc", "lastmod", "changefreq", "priority")
    valid_freqs: ValidFreqs = ("always", "hourly", "daily", "weekly", "monthly", "yearly", "never")

    def __init__(
        self: Url,
        loc: str | None,
        lastmod: str | None = None,
        changefreq: str | None = None,
        priority: str | float | None = None,
    ) -> None:
        """Creates a Url instance.

        Args:
            loc: Location.
            lastmod: Last modified.
            changefreq: Change frequency.
            priority: Priority.
        """
        self.loc = loc
        self.lastmod = lastmod
        self.changefreq = changefreq
        self.priority = float(priority) if priority is not None else None

    @property
    def changefreq(self: Url) -> Freqs | None:
        """Get changefreq."""
        return self._changefreq

    @changefreq.setter
    def changefreq(self: Url, frequency: str | None) -> None:
        """Set changefreq.

        Args:
            self: The Url instance
            frequency: Change frequency.

        Raises:
            ValueError: Value is not an allowed value
        """
        if frequency is not None and frequency not in Url.valid_freqs:
            msg: str = f"'{frequency}' is not an allowed value: {Url.valid_freqs}"
            raise ValueError(msg)
        self._changefreq: Freqs | None = frequency

    @property
    def priority(self: Url) -> float | None:
        """Get priority.

        Returns:
            Priority
        """
        return self._priority

    @priority.setter
    def priority(self: Url, priority: float | None) -> None:
        if priority is not None:
            priority = float(priority)

            min_value = 0.0
            max_value = 1.0
            if priority < min_value or priority > max_value:
                msg: str = f"'{priority}' is not between 0.0 and 1.0"
                raise ValueError(msg)

        self._priority: float | None = priority

    def __str__(self: Url) -> str:
        """Return a string representation of the Url instance.

        Returns:
            String representation of the Url instance
        """
        return self.loc or ""

    def __repr__(self: Url) -> str:
        """Return a string representation of the Url instance.

        Returns:
            String representation of the Url instance
        """
        return f"Url(loc={self.loc}, lastmod={self.lastmod}, changefreq={self.changefreq}, priority={self.priority})"


class UrlSet:
    """Class to represent a <urlset> element."""

    allowed_fields: typing.ClassVar[tuple[str, ...]] = (
        "loc",
        "lastmod",
        "changefreq",
        "priority",
    )

    def __init__(self, urlset_element: Element) -> None:
        """Initialize the UrlSet instance with the <urlset> element."""
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
        url_data: dict[str, str | None] = {}
        for ele in url_element:
            name = ele.xpath("local-name()")  # type: ignore[attr-defined]
            if name in UrlSet.allowed_fields:
                url_data[name] = ele.text

        logger.debug(f"url_data {url_data}")
        return Url(**url_data)

    @staticmethod
    def urls_from_url_set_element(url_set_element: Element) -> Generator[Url, typing.Any, None]:
        """Generator for Url instances from a <urlset> element.

        Args:
            url_set_element: lxml representation of a <urlset> element

        Yields:
            Url instance
        """
        logger.debug(f"urls_from_url_set_element {url_set_element}")

        for url_element in url_set_element:
            yield UrlSet.url_from_url_element(url_element)

    def __iter__(self) -> Iterator[Url]:
        """Generator for Url instances from a <urlset> element.

        Returns:
            Url instance
        """
        return UrlSet.urls_from_url_set_element(self.urlset_element)


class SitemapIndex:
    """Represents a <sitemapindex> element."""

    def __init__(self, index_element: Element) -> None:
        """Initialize the SitemapIndex instance with the <sitemapindex> element."""
        self.index_element: Element = index_element

    @staticmethod
    def sitemap_from_sitemap_element(sitemap_element: Element) -> Sitemap:
        """Creates a Sitemap instance from a <sitemap> element.

        Args:
            sitemap_element: lxml representation of a <sitemap> element
            sitemap_element: xml.etree.ElementTree.Element representation of a <sitemap> element

        Returns:
            Sitemap instance
        """
        sitemap_data: dict[str, str] = {}
        for ele in sitemap_element:
            name = ele.xpath("local-name()")  # type: ignore[attr-defined]
            value: str = ele.text if ele.text is not None else ""  # use the text attribute directly
            sitemap_data[name] = value

        msg = "Returning sitemap object with data: {}"
        logger.debug(msg, sitemap_data)
        return Sitemap(**sitemap_data)

    @staticmethod
    def sitemaps_from_sitemap_index_element(index_element: Element) -> Generator[Sitemap, Any, None]:
        """Generator for Sitemap instances from a <sitemapindex> element.

        Args:
            index_element: lxml representation of a <sitemapindex> element

        Yields:
            Sitemap instance
        """
        logger.debug("Generating sitemaps from %s", index_element)

        # handle child elements, <sitemap>
        sitemaps: list[Element] = index_element.findall("./*")

        for sm_element in sitemaps:
            yield SitemapIndex.sitemap_from_sitemap_element(sm_element)

    def __iter__(self) -> Iterator[Sitemap]:
        """Generator for Sitemap instances from a <sitemapindex> element.

        Args:
            self: The SitemapIndex instance

        Returns:
            Sitemap instance
        """
        return SitemapIndex.sitemaps_from_sitemap_index_element(self.index_element)

    def __str__(self) -> str:  # noqa: D105
        return f"<SitemapIndex: {self.index_element}>"


class SiteMapParser:
    """Parses a sitemap or sitemap index and returns the appropriate object."""

    def __init__(
        self,
        source: str,
        *,
        is_data_string: bool = False,
        should_cache: bool = True,
        cache_dir: Path = Path(".cache"),
    ) -> None:
        """Initialize the SiteMapParser instance with the URI.

        The source can be a URL or a raw XML string. The parser will determine
        whether to download the data or use the provided string.

        Args:
            source: The URL of the sitemap or raw XML string.
            is_data_string: Whether the source is a raw XML string or not.
            should_cache: Whether to cache the request with Hishel (https://hishel.com/) or not.
            cache_dir: The directory to store the cached data.
        """
        self.source: str = source
        self.is_sitemap_index: bool = False
        self._sitemaps: SitemapIndex | None = None
        self._url_set: UrlSet | None = None
        self._should_cache: bool = should_cache
        self._cache_dir: Path = cache_dir
        self._is_data_string: bool = is_data_string
        self._initialize()

    @staticmethod
    def get_hishel_controller() -> hishel.Controller:
        """Get the Hishel default controller.

        Returns:
            The Hishel controller
        """
        return hishel.Controller(
            cacheable_methods=["GET", "HEAD"],
            cacheable_status_codes=[200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501],
        )

    def get_hishel_storage(self) -> hishel.FileStorage:
        """Get the Hishel default storage.

        Returns:
            The Hishel file storage.
        """
        return hishel.FileStorage(base_path=self._cache_dir)

    def get_hishel_client(self) -> hishel.CacheClient:
        """Get the Hishel default client.

        Returns:
            The Hishel client
        """
        controller: hishel.Controller = SiteMapParser.get_hishel_controller()
        storage: hishel.FileStorage = SiteMapParser.get_hishel_storage(self)
        return hishel.CacheClient(controller=controller, storage=storage, timeout=10, http2=True, follow_redirects=True)

    def _initialize(self) -> None:
        """Initialization processing."""
        self._cache_dir.mkdir(parents=True, exist_ok=True)

        # Determine if we're using raw XML data or downloading from a URL
        if self._is_data_string:
            data: bytes = self.source.encode("utf-8")
        else:
            data: bytes = download_uri_data(
                uri=self.source,
                hishel_client=self.get_hishel_client(),
                should_cache=self._should_cache,
            )

        root_element: Element = bytes_to_element(data=data)

        self.is_sitemap_index = self._is_sitemap_index_element(root_element)

        if self.is_sitemap_index:
            logger.info("Root element is sitemap index")
            self._sitemaps = SitemapIndex(index_element=root_element)
        else:
            logger.info("Root element is url set")
            self._url_set = UrlSet(urlset_element=root_element)

    @staticmethod
    def _is_sitemap_index_element(element: Element) -> bool:
        """Determine if the element is a sitemapindex.

        Args:
            element(Element): The element to check

        Returns:
            bool: True if the element is a sitemapindex, False otherwise
        """
        return bool(len(element.xpath("/*[local-name()='sitemapindex']")))  # type: ignore[attr-defined]

    @staticmethod
    def _is_url_set_element(element: Element) -> bool:
        """Determine if the element is a <urlset>.

        Args:
            element: The element to check

        Returns:
            bool: True if the element is a <urlset>, False otherwise
        """
        return bool(len(element.xpath("/*[local-name()='urlset']")))  # type: ignore[attr-defined]

    def get_sitemaps(self) -> SitemapIndex:
        """Retrieve the sitemaps.

        Can check if 'has_sitemaps()' returns True to determine
        if this should be used without calling it

        Raises:
            KeyError: If the root is not a <sitemapindex>

        Returns:
            SitemapIndex: The sitemaps as a SitemapIndex instance
        """
        if not self.has_sitemaps():
            error_msg = "Method called when root is not a <sitemapindex>"
            logger.critical(error_msg)
            raise KeyError(error_msg)

        if self._sitemaps is None:
            msg = "Sitemaps are not available"
            raise KeyError(msg)

        return self._sitemaps

    def get_urls(self) -> UrlSet:
        """Retrieve the urls.

        Raises:
            KeyError: If the root is not a <urlset>

        Returns:
            UrlSet
        """
        if not self.has_urls():
            error_msg = "Method called when root is not a <urlset>"
            logger.critical(error_msg)

            # Check if the root is a <sitemapindex>
            if self.is_sitemap_index:
                error_msg = "Method called when root is a <sitemapindex>. Use 'get_sitemaps()' instead"
            raise KeyError(error_msg)

        if self._url_set is None:
            msg = "URLs are not available"
            raise KeyError(msg)

        return self._url_set

    def has_sitemaps(self) -> bool:
        """Determine if the URL's data contained sitemaps.

        A sitemap can contain other sitemaps. For example: <https://www.webhallen.com/sitemap.xml>


        Returns:
            Boolean
        """
        return self.is_sitemap_index

    def has_urls(self) -> bool:
        """Determine if the URL's data contained urls.

        Returns:
            Boolean
        """
        return not self.is_sitemap_index

    def __str__(self) -> str:
        """String representation of the SiteMapParser instance.

        Returns:
            str
        """
        return str(self._sitemaps if self.has_sitemaps() else self._url_set)


class JSONExporter:
    """Export site map data to JSON format."""

    def __init__(self, data: SiteMapParser) -> None:
        """Initializes the JSONExporter instance with the site map data."""
        self.data: SiteMapParser = data

    @staticmethod
    def _collate(fields: SitemapFields | UrlFields, row_data: SitemapIndex | UrlSet) -> list[dict[str, Any]]:
        """Collate data from SitemapIndex or UrlSet into a list of dictionaries.

        Args:
            fields (SitemapFields | UrlFields): The fields to include in the output.
            row_data (SitemapIndex | UrlSet): An iterable containing Sitemap or Url objects.

        Returns:
            list: A list of dictionaries where each dictionary represents a Sitemap or Url object.
        """
        dump_data: list[dict[str, Any]] = []
        for sm in row_data:
            row: dict[str, Any] = {}
            for fld in fields:
                v = getattr(sm, fld)
                row[fld] = v.isoformat() if isinstance(v, datetime) else v
            dump_data.append(row)
        return dump_data

    def export_sitemaps(self) -> str:
        """Export site map data to JSON format.

        Returns:
            str: JSON data as a string
        """
        try:
            sitemap_fields: SitemapFields = getattr(Sitemap, "fields", ("loc", "lastmod"))  # Default fields
        except AttributeError:
            sitemap_fields: SitemapFields = ("loc", "lastmod")  # Default fields

        return dumps(self._collate(sitemap_fields, self.data.get_sitemaps()))

    def export_urls(self) -> str:
        """Export site map data to JSON format.

        Returns:
            str: JSON data as a string
        """
        try:
            url_fields: UrlFields = getattr(Url, "fields", ("loc", "lastmod", "changefreq", "priority"))
        except AttributeError:
            url_fields: UrlFields = ("loc", "lastmod", "changefreq", "priority")  # Default fields

        return dumps(self._collate(url_fields, self.data.get_urls()))
