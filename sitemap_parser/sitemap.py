from __future__ import annotations

from .base_data import BaseData


class Sitemap(BaseData):
    """Representation of the <sitemap> element."""

    fields = "loc", "lastmod"

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
