# Sitemap Parser

<p align="center">
  <img src="https://github.com/thelovinator1/sitemap-parser/blob/master/.github/logo.png?raw=true" title="Robot searching for sitemaps" alt="Robot searching for sitemaps" width="300" height="300" />
</p>

This is a Python library designed to parse XML sitemaps and sitemap index files from a given URL. It supports both standard XML sitemaps (which contain URLs) and sitemap index files (which contain links to other sitemaps). This tool is useful for extracting data such as URLs and modification dates from website sitemaps.

## Acknowledgments

This is a fork of [Dave O'Connor](https://github.com/daveoconnor)'s [site-map-parser](https://github.com/daveoconnor/site-map-parser). I couldn't have done this without his original work.

## Features

- **Sitemap Parsing**: Extract URLs from standard sitemaps.
- **Sitemap Index Parsing**: Extract links to other sitemaps from sitemap index files.
- **Supports Caching**: Use Hishel for caching responses and reducing redundant requests.
- **Handles Large Sitemaps**: Capable of parsing large sitemaps and sitemap indexes efficiently.
- **Customizable Caching Options**: Option to enable or disable caching while downloading sitemaps.

## Installation

You can install the required dependencies via poetry or pip.

```sh
poetry add git+https://github.com/TheLovinator1/sitemap-parser.git
pip install git+https://github.com/TheLovinator1/sitemap-parser.git
```

## Usage

You can parse sitemaps or sitemap indexes by creating an instance of SiteMapParser and passing the URL of the sitemap or sitemap index.

### Get sitemaps from a sitemap index

```python
from sitemap_parser import SitemapIndex, SiteMapParser

sitemap_url = "https://www.webhallen.com/sitemap.xml"
parser = SiteMapParser(sitemap_url)

if parser.has_sitemaps():
    sitemaps: SitemapIndex = parser.get_sitemaps()
    for sitemap in sitemaps:
        print(sitemap.loc, sitemap.lastmod)
```

### Get URLs from a sitemap

```python
from sitemap_parser import SiteMapParser, UrlSet

sitemap_url = "https://www.webhallen.com/sitemap.infoPages.xml"
parser = SiteMapParser(sitemap_url)

if parser.has_urls():
    urls: UrlSet = parser.get_urls()
    for url in urls:
        print(url.loc, url.lastmod)
```

## Additional Features

### Caching

The parser uses the hishel library for caching by default. You can disable caching if needed by passing the should_cache=False flag when creating the SiteMapParser instance.

```python
parser = SiteMapParser(sitemap_url, should_cache=False)
```

### Configuration

**Caching**: The caching feature uses Hishel, an efficient caching library. You can configure the caching directory or turn off caching completely.

Example:

```python
parser = SiteMapParser(sitemap_url, cache_dir=Path("/path/to/cache"))
```

## Error Handling

**Invalid URLs**: If an invalid URL is provided, a ValueError will be raised.
**Parsing Errors**: If the XML sitemap or sitemap index is malformed, an XML parsing error will be logged.

## Contributing

Contributions are welcome! If you'd like to improve this project, feel free to submit a pull request. Please follow the guidelines below:

1. Fork the Repository
2. Create a New Branch
3. Submit a Pull Request

## License

This project is licensed under the MIT License.

## Contact

If you have any questions or suggestions, please open an issue on the GitHub repository. You can also reach me via email at [tlovinator@gmail.com](mailto:tlovinator@gmail.com) or on Discord at TheLovinator#9276.

Happy parsing!
