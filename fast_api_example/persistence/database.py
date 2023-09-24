from abc import ABC, abstractmethod


class Database(ABC):
    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def get_metadata(self):
        pass
