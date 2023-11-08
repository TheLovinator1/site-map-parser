from __future__ import annotations

import pytest

from sitemapparser.exporter import Exporter


class TestExporter:
    """Test Exporter class."""

    def setup(self: TestExporter) -> None:
        """Setup for TestExporter.

        Args:
            self: TestExporter
        """
        self.test_data: list[str] = ["foo", "bar"]

    def test_abstract(self: TestExporter) -> None:
        """Test that Exporter is an abstract class.

        Args:
            self: TestExporter
        """
        with pytest.raises(TypeError):
            Exporter(self.test_data)  # type: ignore  # noqa: PGH003

        assert "short_name" in Exporter.__abstractmethods__
        assert "export_sitemaps" in Exporter.__abstractmethods__
        assert "export_urls" in Exporter.__abstractmethods__

        # test that they're not implemented
        Exporter.__abstractmethods__ = frozenset()
        e = Exporter(self.test_data)  # type: ignore # noqa: PGH003
        with pytest.raises(NotImplementedError):
            e.short_name  # noqa: B018
        with pytest.raises(NotImplementedError):
            e.export_sitemaps()
        with pytest.raises(NotImplementedError):
            e.export_urls()
