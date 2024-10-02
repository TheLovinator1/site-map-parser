from __future__ import annotations

from typing import Literal

from .base_data import BaseData

Freqs = Literal["always", "hourly", "daily", "weekly", "monthly", "yearly", "never"]
ValidFreqs = tuple[Freqs, Freqs, Freqs, Freqs, Freqs, Freqs, Freqs]
Fields = tuple[Literal["loc"], Literal["lastmod"], Literal["changefreq"], Literal["priority"]]


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
        priority: float | None = None,
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
        self.priority = priority

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
