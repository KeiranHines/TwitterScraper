import unittest
from datetime import datetime

from src.twitter import TweetData


class TweetDataTestCase(unittest.TestCase):
    def test_to_string(self):
        date = datetime.fromtimestamp(667040400)
        dummy_data = TweetData('Some Author', 'A message to the people', date)
        self.assertEqual(str(dummy_data), '| 1991-02-20 | Some Author | A message to the people')


if __name__ == '__main__':
    unittest.main()
