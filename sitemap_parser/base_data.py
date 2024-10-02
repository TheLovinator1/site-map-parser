from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from dateutil import parser

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(slots=True)
class BaseData:
    """Base class for sitemap data.

    Provides common properties and methods for sitemap and sitemap index entries,
    such as location (`loc`) and last modified time (`lastmod`).
    """

    _lastmod: datetime | None = field(default=None, init=False)
    _loc: str | None = field(default=None, init=False)

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
        if not re.match("http[s]?://", value):
            msg: str = f"{value} is not a valid URL"
            raise ValueError(msg)

        # Set the value
        self._loc = value
