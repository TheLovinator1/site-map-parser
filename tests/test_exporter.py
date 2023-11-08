import pytest

from sitemapparser.exporter import Exporter


class TestExporter:
    def setup(self):
        self.test_data = ["foo", "bar"]

    def test_abstract(self):
        # test that this is an abstract class overall
        with pytest.raises(TypeError):
            Exporter(self.test_data)

        assert "short_name" in Exporter.__abstractmethods__
        assert "export_sitemaps" in Exporter.__abstractmethods__
        assert "export_urls" in Exporter.__abstractmethods__

        # test that they're not implemented
        Exporter.__abstractmethods__ = frozenset()
        e = Exporter(self.test_data)
        with pytest.raises(NotImplementedError):
            e.short_name
        with pytest.raises(NotImplementedError):
            e.export_sitemaps()
        with pytest.raises(NotImplementedError):
            e.export_urls()
