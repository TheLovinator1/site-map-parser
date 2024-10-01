from __future__ import annotations


def uri_modifier(url: str) -> str:
    """Modify the uri to be a valid sitemap.xml url.

    Args:
        url: Url to be modified

    Returns:
        Modified url
    """
    if not url.startswith("https://") and not url.startswith("http://"):
        url = "http://" + url

    if not url.endswith(".xml"):
        if not url.endswith("/"):
            url += "/"
        url += "sitemap.xml"
    return url
