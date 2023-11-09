# Sitemap Parser

## Installation

```sh
poetry add git+https://github.com/TheLovinator1/site-map-parser.git
pip install git+https://github.com/TheLovinator1/site-map-parser.git
```

## Usage

### Get sitemaps from a sitemap

In this example we will use <https://www.webhallen.com/sitemap.xml>.

```python
def get_sitemaps() -> None:
    """If we want to get the sitemaps from another sitemap, we can do it like this."""
    sm = SiteMapParser("https://www.webhallen.com/sitemap.xml")
    if sm.has_sitemaps():
        # This will alway be true because the sitemap at https://www.webhallen.com/sitemap.xml has other sitemaps inside it.

        sitemaps: SitemapIndex = sm.get_sitemaps()
        logger.info("get_sitemaps():")
        for sitemap in sitemaps:
            logger.info(f"\t{sitemap=}")
            """
            get_sitemaps():
                sitemap=<Sitemap https://www.webhallen.com/sitemap.home.xml>
                sitemap=<Sitemap https://www.webhallen.com/sitemap.section.xml>
                sitemap=<Sitemap https://www.webhallen.com/sitemap.category.xml>
                sitemap=<Sitemap https://www.webhallen.com/sitemap.campaign.xml>
                sitemap=<Sitemap https://www.webhallen.com/sitemap.campaignList.xml>
                sitemap=<Sitemap https://www.webhallen.com/sitemap.infoPages.xml>
                sitemap=<Sitemap https://www.webhallen.com/sitemap.product.xml>
                sitemap=<Sitemap https://www.webhallen.com/sitemap.manufacturer.xml>
                sitemap=<Sitemap https://www.webhallen.com/sitemap.article.xml>
            """
```

### Get URLs from a sitemap

In this example we will use <https://www.webhallen.com/sitemap.article.xml>

```python
def get_urls() -> None:
    """Get the urls from a sitemap."""
    sm = SiteMapParser("https://www.webhallen.com/sitemap.article.xml")
    urls: UrlSet = sm.get_urls()
    logger.info("get_urls():")
    for url in urls:
        logger.info(f"\t{url=}")
        # Result:
        """
        get_urls():
            url=Url(loc=https://www.webhallen.com/se/article/2-Covid-19-Butiksatgarder, lastmod=None, changefreq=None, priority=0.3)
            url=Url(loc=https://www.webhallen.com/se/article/4-Tre-enkla-steg-for-ett-smart-hem, lastmod=None, changefreq=None, priority=0.3)
            url=Url(loc=https://www.webhallen.com/se/article/5-Bast-laptop-for-varterminen-2021, lastmod=None, changefreq=None, priority=0.3)
        ... truncated ...
        """
```

### JSON Exporter

You can also export the sitemap to JSON:

```python
def get_json() -> None:
    sm = SiteMapParser("https://www.webhallen.com/sitemap.article.xml")
    json_exporter = JSONExporter(sm)
    if sm.has_sitemaps():
        # Note: This will not be triggered in this example since the sitemap
        # does not have any sitemaps.
        sitemaps_json: str = json_exporter.export_sitemaps()
        logger.info(f"{sitemaps_json=}")

    elif sm.has_urls():
        urls_json: str = json_exporter.export_urls()
        urls_json = json.loads(urls_json)
        logger.info(json.dumps(urls_json, indent=4))
        # Result:
        """
        [
            {
                "loc": "https://www.webhallen.com/se/article/2-Covid-19-Butiksatgarder",
                "lastmod": null,
                "changefreq": null,
                "priority": 0.3
            },
            {
                "loc": "https://www.webhallen.com/se/article/4-Tre-enkla-steg-for-ett-smart-hem",
                "lastmod": null,
                "changefreq": null,
                "priority": 0.3
            },
            ... truncated ...
        ]
        """
```
