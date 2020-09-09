from abc import ABC, abstractmethod

from . import AbstractDataClass


class IHandler(ABC):
    """ Base class for a generic data handler to process messages scraped into AbstractDataClass objects. """

    @abstractmethod
    def process(self, data: AbstractDataClass):
        """Processes the data received.
        This method should be fail-safe, that is, any exceptions should be handled within this method and not bubbled up.
        :param data: The data to process.
        :return: None
        """
        pass
