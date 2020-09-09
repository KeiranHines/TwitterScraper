from src.framework.IHandler import IHandler
from src.framework import AbstractDataClass


class StdOutHandler(IHandler):
    """ Handles new Abstract data messages by printing them to stdout. """
    def __init__(self):
        super().__init__()

    def process(self, data: AbstractDataClass):
        """ Prints the incoming data to stdOut removing any newlines and replacing them with spaces.
        :param data: The data to print.
        :return: None.
        """
        print(str(data).replace('\n', ' '))
