import re
from abc import ABCMeta

from dateutil import parser


class BaseData(metaclass=ABCMeta):
    def __init__(self):
        self._lastmod = None
        self._loc = None

    @property
    def lastmod(self):
        return self._lastmod

    @lastmod.setter
    def lastmod(self, value):
        self._lastmod = parser.isoparse(value) if value is not None else None

    @property
    def loc(self):
        return self._loc

    @loc.setter
    def loc(self, value):
        value = str(value)
        if not re.match("http[s]?://", value):
            raise ValueError("{} does not match a url".format(value))
        self._loc = value
