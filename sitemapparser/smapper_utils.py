from __future__ import annotations

from pathlib import Path


def get_logging_config() -> tuple[str, str]:
    """Get the logging config file and log file.

    Returns:
        Tuple of logging config file and log file.
    """
    log_config: Path = Path(__file__).parent / "logging_config.ini"
    log_file: Path = Path.expanduser(Path("~")) / "sitemap_run.log"

    return str(log_config), str(log_file)


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
            url = url + "/"
        url = url + "sitemap.xml"
    return url
