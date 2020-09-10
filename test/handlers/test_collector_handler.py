import unittest
from src.handlers import CollectorHandler
from test.mocks import MockDataClass
from datetime import datetime


class CollectorHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.collector = CollectorHandler()

    def test_getting_single_history_json(self):
        datetime1 = datetime.fromtimestamp(1599691801)
        message1 = MockDataClass("Author", "First Message", datetime1)
        self.collector.process(message1)

        expected_json = '{'\
                        '"messages": ['\
                        '{"author": "Author", "content": "First Message", "timestamp": "2020-09-10 08:50:01"}'\
                        ']}'
        self.assertEqual(str(self.collector.as_json()), expected_json)

    def test_getting_multiple_history_json(self):
        datetime1 = datetime.fromtimestamp(1599691801)
        datetime2 = datetime.fromtimestamp(1599690000)
        message1 = MockDataClass("Author", "First Message", datetime1)
        message2 = MockDataClass("Author", "Second Message", datetime2)
        self.collector.process(message1)
        self.collector.process(message2)

        expected_json = '{'\
                        '"messages": ['\
                        '{"author": "Author", "content": "First Message", "timestamp": "2020-09-10 08:50:01"},'\
                        ' {"author": "Author", "content": "Second Message", "timestamp": "2020-09-10 08:20:00"}'\
                        ']}'
        self.assertEqual(self.collector.as_json(), expected_json)

if __name__ == '__main__':
    unittest.main()
