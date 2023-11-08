# Site Map Parser

Script and library which reads urls and converts to objects, allows exporting as CSV or JSON.

Handle sitemaps according to: <https://www.sitemaps.org/protocol.html>

## Installation

```sh
pip install site-map-parser
```

## Usage

### Script usage

```sh
smapper $url > /tmp/data.csv
```

Logs written to ~/sitemap_run.log

#### Arguments

| Argument | Options| Default  |  Information|
| ----------- | ----------- | ----------- | -----------|
| -h | N/A | N/A | Outputs argument data |
| url | e.g. `http://www.example.com` - `http://www.example.com/other_sitemap.xml` | N/A | Required - sitemap data to retrieve |
| -l, --log | `CRITICAL` or `ERROR` or `WARNING` or `INFO` or `DEBUG` | `INFO` | logs to sitemapper_run.log in install folder |
| -e, --exporter | `csv` or `json` | `csv` | Export format of the data |

### Library Usage

```python
from sitemapparser import SiteMapParser

sm = SiteMapParser('http://www.example.com')    # reads /sitemap.xml
if sm.has_sitemaps():
    sitemaps = sm.get_sitemaps() # returns iterator of sitemapper.Sitemap instances
else:
    urls = sm.get_urls()         # returns iterator of sitemapper.Url instances
```

#### Exporting

Two exporters are available: csv and json

##### CSV Exporter

```python
from sitemapparser.exporters import CSVExporter

# sm set as per earlier library usage example

csv_exporter = CSVExporter(sm)
if sm.has_sitemaps():
    print(csv_exporter.export_sitemaps())
elif sm.has_urls():
    print(csv_exporter.export_urls())
```

##### JSON Exporter

```python
from sitemapparser.exporters import JSONExporter

# sm set as per earlier library usage example

json_exporter = JSONExporter(sm)
if sm.has_sitemaps():
    print(json_exporter.export_sitemaps())
elif sm.has_urls():
    print(json_exporter.export_urls())
```
