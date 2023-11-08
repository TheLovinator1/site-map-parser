from __future__ import annotations

from abc import ABCMeta, abstractmethod, abstractproperty
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sitemapparser.base_data import BaseData


class Exporter(metaclass=ABCMeta):
    """Base class for all exporters."""

    def __init__(self: Exporter, data: BaseData) -> None:
        """Constructor for Exporter.

        Args:
            data: The data to export
        """
        self.data: BaseData = data

    @abstractproperty
    def short_name(self: Exporter):  # noqa: ANN201
        """Name which will be passed as an argument as the 'exporter', .e.g 'csv'."""
        raise NotImplementedError

    @abstractmethod
    def export_sitemaps(self: Exporter):  # noqa: ANN201
        """Should output the formatted data of self.data.get_sitemaps()."""
        raise NotImplementedError

    @abstractmethod
    def export_urls(self: Exporter):  # noqa: ANN201
        """Should output the formatted data of self.data.get_urls()."""
        raise NotImplementedError
