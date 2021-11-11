from abc import ABC, abstractmethod

class StorageInterface(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_download_list(self, count:int) ->list:
        pass

    @abstractmethod
    def add(self, element):
        pass

    @abstractmethod
    def add_to_download(self, elements):
        pass
