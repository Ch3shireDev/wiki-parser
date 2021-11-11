from abc import ABC, abstractmethod


class DownloaderInterface(ABC):

    @abstractmethod
    def download(self, url):
        pass
