from abc import ABC, abstractmethod

from src.framework import AbstractDataClass


class IHandler(ABC):
    """ Interface for a generic data handler to process messages scraped into AbstractDataClass objects. """
    @abstractmethod
    def process(self, data: AbstractDataClass):
        pass
