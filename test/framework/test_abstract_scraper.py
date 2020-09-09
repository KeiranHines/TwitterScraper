import unittest
from datetime import datetime


from test.mocks import MockScraper, MockHandler, MockDataClass


class AbstractScraperTestCase(unittest.TestCase):
    def setUp(self):
        self.scraper = MockScraper("mock")
        self.handler = MockHandler()
        self.mock_data = MockDataClass("mock", "mock message", datetime.now())

    def test_handler_registration(self):
        self.scraper.register_handler(self.handler)
        self.assertEqual(self.handler.get_count(), 0, "Count is not at initial state")

        self.scraper._notify_handlers(self.mock_data)
        self.assertEqual(self.handler.get_count(), 1, "Handler failed to receive the message")

        self.scraper._notify_handlers(self.mock_data)
        self.assertEqual(self.handler.get_count(), 2, "Handler failed to receive a second message")

    def test_handler_cannot_register_twice(self):
        self.scraper.register_handler(self.handler)
        self.scraper.register_handler(self.handler)
        self.assertEqual(self.handler.get_count(), 0, "Count is not at initial state")

        self.scraper._notify_handlers(self.mock_data)
        self.assertEqual(self.handler.get_count(), 1, "Handler should have only registered once and received one message")

        self.scraper._notify_handlers(self.mock_data)
        self.assertEqual(self.handler.get_count(), 2, "Handler failed to receive a second message")

    def test_multiple_hanlders_can_register(self):
        self.scraper.register_handler(self.handler)
        handler2 = MockHandler()
        self.scraper.register_handler(handler2)
        self.assertEqual(self.handler.get_count(), 0, "Count is not at initial state")

        self.scraper._notify_handlers(self.mock_data)
        self.assertEqual(self.handler.get_count(), 1, "Handler should have only registered once and received one message")
        self.assertEqual(handler2.get_count(), 1, "Second handler should have only registered once and received one message")

        self.scraper._notify_handlers(self.mock_data)
        self.assertEqual(self.handler.get_count(), 2, "Handler failed to receive a second message")
        self.assertEqual(handler2.get_count(), 2, "Second handler failed to receive a second message")

    def test_handler_removal(self):
        self.scraper.register_handler(self.handler)
        self.assertEqual(self.handler.get_count(), 0, "Count is not at initial state")

        self.scraper._notify_handlers(self.mock_data)
        self.assertEqual(self.handler.get_count(), 1, "Handler failed to receive the message")

        self.scraper.remove_handler(self.handler)
        self.assertEqual(self.handler.get_count(), 1, "Handler Should not have received the new message, it was removed")


if __name__ == '__main__':
    unittest.main()
