from __future__ import annotations


def ensure_sitemap_url_format(url: str, default_scheme: str = "https://") -> str:
    """Ensure the URL starts with `http://` or `https://` and ends with `sitemap.xml`.

    Args:
        url: A string representing a URL to be modified
        default_scheme: The default scheme to use if the URL does not start with `http://` or `https://`

    Returns:
        Modified url
    """
    # Ensure the URL starts with `http://` or `https://`
    if not url.startswith(("https://", "http://")):
        url = default_scheme + url

    # Ensure the URL ends with `sitemap.xml`
    if not url.endswith("sitemap.xml"):
        url = url.rstrip("/") + "/sitemap.xml"

    return url
