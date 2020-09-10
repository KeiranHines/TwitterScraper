import json
from typing import List

from src.framework import AbstractDataClass
from src.framework.abstract_handler import IHandler


class CollectorHandler(IHandler):
    """ Handles new Abstract data messages by storing them in a list. """

    def __init__(self):
        super().__init__()
        # List is used instead of a database as a proof of concept.
        self.messages: List[AbstractDataClass] = list()

    def process(self, data: AbstractDataClass):
        self.messages.append(data)

    def as_json(self):
        messages = [message.as_dict() for message in self.messages]
        return json.dumps(dict(messages=messages))
