from abc import ABC, abstractmethod
from typing import Set

from src.framework import IHandler


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
