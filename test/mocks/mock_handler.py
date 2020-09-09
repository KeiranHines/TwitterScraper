from src.framework import IHandler, AbstractDataClass


class MockHandler(IHandler):
    """ Class to mock a handler, each new message will add the message to an array """
    def __init__(self):
        self.messages = []

    def process(self, data: AbstractDataClass):
        self.messages.append(data)

    def get_count(self):
        """ Convenience to check messages received """
        return len(self.messages)
