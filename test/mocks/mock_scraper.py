from src.framework import AbstractScraper


class MockScraper(AbstractScraper):
    def __init__(self, target: str):
        super().__init__(target)

    """ Class for mocking a Scraper to test the framework. """
    def get_latest(self, count: int = 1):
        pass

    def update(self):
        pass
