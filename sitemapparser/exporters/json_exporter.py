from datetime import datetime
from json import dumps

from ..exporter import Exporter
from ..sitemap import Sitemap
from ..url import Url


class JSONExporter(Exporter):
    short_name = "json"

    def _collate(self, fields, row_data):
        dump_data = []
        for sm in row_data:
            row = {}
            for field in fields:
                v = getattr(sm, field)
                row[field] = v if type(v) is not datetime else v.isoformat()
            dump_data.append(row)
        return dump_data

    def export_sitemaps(self):
        return dumps(self._collate(Sitemap.fields, self.data.get_sitemaps()))

    def export_urls(self):
        return dumps(self._collate(Url.fields, self.data.get_urls()))
