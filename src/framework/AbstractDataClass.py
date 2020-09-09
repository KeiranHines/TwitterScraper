from abc import ABC
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AbstractDataClass(ABC):
    """ Base data class for tracking messages scraper from various sources. """

    def __init__(self, author: str, content: str, timestamp: datetime):
        self.author = author
        self.content = content
        self.timestamp = timestamp

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author: str):
        self._author = author

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content: str):
        self._content = content

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime):
        self._timestamp = timestamp

    def __str__(self):
        return str(self.timestamp) + ", " + self.author + ", " + self.content
