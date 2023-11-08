from abc import ABCMeta, abstractmethod, abstractproperty


class Exporter(metaclass=ABCMeta):
    def __init__(self, data):
        self.data = data

    @abstractproperty
    def short_name(self):
        """Name which will be passed as an argument as the 'exporter', .e.g 'csv'"""
        raise NotImplementedError

    @abstractmethod
    def export_sitemaps(self):
        """Should output the formatted data of self.data.get_sitemaps()"""
        raise NotImplementedError

    @abstractmethod
    def export_urls(self):
        """Should output the formatted data of self.data.get_urls()"""
        raise NotImplementedError
