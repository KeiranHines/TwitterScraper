from datetime import datetime

from src.framework import AbstractDataClass


class TweetData(AbstractDataClass):
    def __init__(self, author: str, content: str, timestamp: datetime):
        super(TweetData, self).__init__(author, content, timestamp)
        # Improvement: add Any Twitter specifics
