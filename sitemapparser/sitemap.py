from dateutil import parser

from .base_data import BaseData


class Sitemap(BaseData):
    fields = "loc", "lastmod"

    def __init__(self, loc, lastmod=None):
        """
        Representation of the <sitemap> element
        :param loc: String of the url
        :param lastmod: DateTime, The date of last modification of the file.
        """
        self.loc = loc
        self.lastmod = lastmod

    def __str__(self):
        return self.loc
