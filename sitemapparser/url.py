from __future__ import annotations

from typing import Literal

from .base_data import BaseData


class Url(BaseData):
    """Representation of the <url> element.

    Args:
        BaseData: Base class for all data classes

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        _description_
    """

    fields: tuple[
        Literal["loc"],
        Literal["lastmod"],
        Literal["changefreq"],
        Literal["priority"],
    ] = "loc", "lastmod", "changefreq", "priority"
    valid_freqs: tuple[
        Literal["always"],
        Literal["hourly"],
        Literal["daily"],
        Literal["weekly"],
        Literal["monthly"],
        Literal["yearly"],
        Literal["never"],
    ] = ("always", "hourly", "daily", "weekly", "monthly", "yearly", "never")

    def __init__(
        self: Url,
        loc: str | None,
        lastmod: str | None = None,
        changefreq: str | None = None,
        priority: float | None = None,
    ) -> None:
        """Creates a Url instance.

        Args:
            self: The Url instance
            loc: Location.
            lastmod: Last modified.
            changefreq: Change frequency.
            priority: Priority.
        """
        self.loc = loc
        self.lastmod = lastmod
        self.changefreq = changefreq
        self.priority = priority

    @property
    def changefreq(
        self: Url,
    ) -> (
        Literal["always", "hourly", "daily", "weekly", "monthly", "yearly", "never"]
        | None
    ):
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
            error_msg = "'{}' is not an allowed value: {}"
            raise ValueError(error_msg.format(frequency, Url.valid_freqs))
        self._changefreq: (
            Literal["always", "hourly", "daily", "weekly", "monthly", "yearly", "never"]
            | None
        ) = frequency

    @property
    def priority(self: Url) -> float | None:
        """Get priority.

        Args:
            self: The Url instance

        Returns:
            Priority
        """
        return self._priority

    @priority.setter
    def priority(self: Url, priority: float | None) -> None:
        if priority is not None:
            priority = float(priority)
            if priority < 0.0 or priority > 1.0:  # noqa: PLR2004
                msg = "'{}' is not between 0.0 and 1.0"
                raise ValueError(msg)
        self._priority: float | None = priority

    def __str__(self: Url) -> str:
        """Return a string representation of the Url instance.

        Args:
            self: The Url instance

        Returns:
            String representation of the Url instance
        """
        return self.loc or ""
