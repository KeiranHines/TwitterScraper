from datetime import datetime

from src.framework import AbstractDataClass


class MockDataClass(AbstractDataClass):
    def __init__(self, author: str, content: str, timestamp: datetime):
        super().__init__(author, content, timestamp)
