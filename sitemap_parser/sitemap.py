from __future__ import annotations

from .base_data import BaseData


class Sitemap(BaseData):
    """Representation of the <sitemap> element.

    Args:
        BaseData: Base class for all data classes.

    Returns:
        Sitemap instance
    """

    fields = "loc", "lastmod"

    def __init__(self: Sitemap, loc: str, lastmod: str | None = None) -> None:
        """Representation of the <sitemap> element.

        Args:
            loc: String, URL of the page.
            lastmod: DateTime, The date of last modification of the file.
        """
        self.loc = loc
        self.lastmod = lastmod

    def __str__(self: Sitemap) -> str | None:
        """String representation of the Sitemap instance.

        Returns:
            String
        """
        return self.loc

    def __repr__(self: Sitemap) -> str:
        """Representation of the Sitemap instance.

        Returns:
            String
        """
        return f"<Sitemap {self.loc}>"
