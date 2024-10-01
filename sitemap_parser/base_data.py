from __future__ import annotations

import re
from typing import TYPE_CHECKING

from dateutil import parser

if TYPE_CHECKING:
    from datetime import datetime


class BaseData:
    """Base class for Sitemap and SitemapIndex.

    Args:
        metaclass: ABCMeta
    """

    def __init__(self: BaseData) -> None:
        """Constructor for BaseData.

        Args:
            self: The BaseData object
        """
        self._lastmod: datetime | None = None
        self._loc: str | None = None

    @property
    def lastmod(self: BaseData) -> datetime | None:
        """Lastmod property.

        Args:
            self: The BaseData object

        Returns:
            When last modified
        """
        return self._lastmod

    @lastmod.setter
    def lastmod(self: BaseData, value: str | None) -> None | datetime:
        """Lastmod setter.

        Parse an ISO-8601 datetime string into a datetime object.

        Args:
            self: The BaseData object
            value: The value to set
        """
        self._lastmod: datetime | None = parser.isoparse(value) if value is not None else None

    @property
    def loc(self: BaseData) -> str | None:
        """Loc property.

        Args:
            self: The BaseData object

        Returns:
            The location
        """
        return self._loc

    @loc.setter
    def loc(self: BaseData, value: str | None) -> None:
        """Loc setter.

        Args:
            value: The value to set

        Raises:
            ValueError: If the value is not a url
        """
        value = str(value)
        if not re.match("http[s]?://", value):
            msg: str = f"{value} does not match a url"
            raise ValueError(msg)
        self._loc = value
