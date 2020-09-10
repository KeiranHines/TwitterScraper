import unittest
from datetime import datetime

from src.twitter import TweetData


class TweetDataTestCase(unittest.TestCase):
    def test_to_string(self):
        date = datetime.fromtimestamp(667040400)
        dummy_data = TweetData('Some Author', 'A message to the people', date)
        self.assertEqual(str(dummy_data), '| 1991-02-20 | Some Author | A message to the people')

    def test_to_json(self):
        date = datetime.fromtimestamp(667040400)
        dummy_data = TweetData('Some Author', 'A message to the people', date)
        expected_json = '{'\
                        '"author": "Some Author",'\
                        ' "content": "A message to the people",' \
                        ' "timestamp": "1991-02-20 20:00:00"' \
                        '}'
        print(dummy_data.as_json())
        self.assertEqual(dummy_data.as_json(), expected_json)


if __name__ == '__main__':
    unittest.main()
