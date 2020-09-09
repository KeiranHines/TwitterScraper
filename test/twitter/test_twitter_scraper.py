import unittest
from unittest import mock
from datetime import datetime

from src.twitter import TwitterScraper


class TwitterScraperTestCase(unittest.TestCase):
    def setUp(self):
        self.scraper = TwitterScraper("Twitter")

    def test_calling_get_latest_calls_with_limit(self):
        self.scraper._get_data = mock.MagicMock()
        self.scraper.get_latest(5)
        self.scraper._get_data.assert_called_once_with(limit=5)

        self.scraper.get_latest(10)
        self.scraper._get_data.assert_called_with(limit=10)

    def test_calling_update_will_use_last_read(self):
        timestamp = datetime.fromtimestamp(1599691801)
        self.scraper.last_read = timestamp
        self.scraper._get_data = mock.MagicMock()
        self.scraper.update()
        self.scraper._get_data.assert_called_once_with(timestamp)

        timestamp = datetime.fromtimestamp(1599000000)
        self.scraper.last_read = timestamp
        self.scraper.update()
        self.scraper._get_data.assert_called_with(timestamp)


if __name__ == '__main__':
    unittest.main()
