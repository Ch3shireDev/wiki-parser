from abc import ABC, abstractmethod

class ServiceInterface(ABC):

    @abstractmethod
    def download_next(self):
        pass
