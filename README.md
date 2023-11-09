# Sitemap Parser

## Installation

```sh
pip install site-map-parser
```

## Usage

```python
from sitemap_parser import SiteMapParser

sm = SiteMapParser("http://panso.se/sitemap.xml")
if sm.has_sitemaps():
    sitemaps = sm.get_sitemaps() # returns iterator of sitemapper.Sitemap instances
else:
    urls = sm.get_urls()         # returns iterator of sitemapper.Url instances
```

#### Exporting

Two exporters are available: csv and json

##### CSV Exporter

```python
from sitemap_parser.exporters import CSVExporter

# sm set as per earlier library usage example

csv_exporter = CSVExporter(sm)
if sm.has_sitemaps():
    print(csv_exporter.export_sitemaps())
elif sm.has_urls():
    print(csv_exporter.export_urls())
```

##### JSON Exporter

```python
from sitemap_parser.exporters import JSONExporter

# sm set as per earlier library usage example

json_exporter = JSONExporter(sm)
if sm.has_sitemaps():
    print(json_exporter.export_sitemaps())
elif sm.has_urls():
    print(json_exporter.export_urls())
```
