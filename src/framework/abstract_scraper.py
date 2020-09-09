from abc import ABC, abstractmethod
from typing import Set

from . import IHandler, AbstractDataClass


class AbstractScraper(ABC):
    """ Abstract class for defining the skeleton of a data scraper. """

    def __init__(self, target: str):
        self.target = target
        self.last_read = None
        self.handlers: Set[IHandler] = set()

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target: str):
        self._target = target

    @abstractmethod
    def get_latest(self, count: int = 1):
        pass

    @abstractmethod
    def update(self):
        pass

    def register_handler(self, handler: IHandler):
        """ Registers a handler to process any new tweets.
        :param handler: IHandler - The handler to register for updates.
        :return: None
        """
        self.handlers.add(handler)

    def remove_handler(self, handler: IHandler):
        """ Removes an existing handler from the twitter to be updated when a new tweet is processed.
        :param handler: IHandler - The handler to remove.
        :return: None
        """
        self.handlers.remove(handler)

    def _notify_handlers(self, data: AbstractDataClass):
        """ Notifies all all handlers of a new tweet.
        :param data: The tweet to notify about.
        :return: None
        """
        if data is None:
            return
        for handler in self.handlers:
            handler.process(data)
