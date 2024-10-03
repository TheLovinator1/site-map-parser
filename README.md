# Sitemap Parser

<p align="center">
  <img src="https://github.com/thelovinator1/sitemap-parser/blob/master/.github/logo.png?raw=true" title="Robot searching for sitemaps" alt="Robot searching for sitemaps" width="300" height="300" />
</p>

This Python library is designed to scrape sitemaps from websites, providing a simple and efficient way to gather information about the structure of a website.

## Acknowledgments

This is a fork of [Dave O'Connor](https://github.com/daveoconnor)'s [site-map-parser](https://github.com/daveoconnor/site-map-parser). I couldn't have done this without his original work.

## Installation

```sh
poetry add git+https://github.com/TheLovinator1/sitemap-parser.git
pip install git+https://github.com/TheLovinator1/sitemap-parser.git
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

### Contributing

Feel free to contribute to this project by creating a pull request or an issue.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
