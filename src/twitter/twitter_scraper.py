import logging
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.framework import AbstractScraper
from src.framework.exceptions import NoUserFoundException
from . import TweetData


class TwitterScraper(AbstractScraper):
    """ Twitter scrapper to pull the time, contents and user from a Twitter feed. """

    def __init__(self, target: str):
        super(TwitterScraper, self).__init__(target)

    def get_latest(self, count: int = -1):
        """ Gets the latest N tweets from the user  where N is the count, and broadcasts them to all twitter.
        :param count: int - The number of tweets to get.
        :return: None
        """
        self._get_data(limit=count)

    def update(self):
        """ Updates all twitter with any new tweets that have arrived since last update.
        :return: None
        """
        self._get_data(self.last_read)

    def _get_data(self, timestamp: datetime = None, limit: int = -1):
        """ Scrapes the twitter feed of the user to find any new tweets up to the limit or timestamp specified.
        :param timestamp: datetime - The timestamp to restrict search to or None for no time restriction, defaults: None
        :param limit: The limit to the number of new tweets to broadcast or -1 for unlimited, defaults: -1
        :return: None
        """
        if datetime is None and limit == -1:
            logging.warning("_get_data called without a limit or datetime restriction")
            return
        since = TIME_PREFIX + timestamp.strftime(SEARCH_TIME_FORMAT) if timestamp else ''
        driver = self._load_driver(self.target, since)
        if driver is None:
            return
        count = 0
        seen = []
        while True:
            raw_feed = driver.find_elements_by_css_selector(TWEET_IDENTIFIER)
            unseen = set(set(raw_feed) - set(seen))
            if len(unseen) == 0:
                logging.debug("End of search reached, no more tweets to process for %s", self.target)
                return
            seen.extend(unseen)
            for tweet in unseen:
                try:
                    data = self.parse_tweet(tweet)
                    # We have reached a timestamp equal or before the requested, stop processing.
                    if (timestamp is not None and data.timestamp <= timestamp) or -1 < limit <= count:
                        driver.close()
                        return
                    self._notify_handlers(data)
                except NoSuchElementException:
                    logging.warning("Could not process tweet, tweet is invalid")
                count += 1
            # Have not found all the tweets we want, scroll down
            driver.execute_script('window.scrollBy(0,1080)')

    @staticmethod
    def _load_driver(username: str, since: str):
        """ Loads WebDriver for scraping tweets and validates the page has loaded some tweets.
        :param username: str - The username to load tweets for.
        :param since: datetime - The time to load tweets since.
        :return: WebDriver - the webdriver to scrape tweets from or None if tweets cannot be scraped.
        :raises: NoUserFoundException - If the load parameters return a search with no tweets.
        """
        url = BASE_URL.format(username=username, since=since)
        driver = None
        try:
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options)
            driver.set_window_size(1920, 1080)
            driver.get(url)
            waiter = WebDriverWait(driver, 5)
            # TODO Better handle No Result and empty result searches.
            waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, TWEET_IDENTIFIER)))
            return driver
        except WebDriverException as ex:
            logging.fatal('Error opening webDriver: (%s)', ex.msg)
            if driver is not None:
                driver.close()
            if isinstance(ex, TimeoutException):
                logging.fatal("Could not find user %s", username)
                raise NoUserFoundException
        return None

    def parse_tweet(self, tweet: WebDriver):
        """ parses a tweet to a TweetData object and updates last_read if the tweet is newer than the last seen.
        :param tweet: WebDriver - element to extract tweet data from.
        :return: TweetData - A dataclass representing the elements of the tweet.
        """
        # Improvement: Add support for extracting tweet id
        time = tweet.find_element_by_tag_name('time').get_attribute('datetime')
        timestamp = datetime.strptime(time, TIME_FORMAT)
        content = ""
        for line in tweet.find_elements_by_css_selector(CONTENT_SELECTOR):
            content += str(line.text)
        # Updating value of the latest we have seen to be able to use of repeat calls
        if self.last_read is None or timestamp > self.last_read:
            self.last_read = timestamp
        data = TweetData(self.target, content, timestamp)
        return data


CONTENT_SELECTOR = 'div[lang=en] > span'
SEARCH_TIME_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
TIME_PREFIX = '%20since%3A'
BASE_URL: str = 'https://twitter.com/search?lang=en&q=(from%3A{username}){since}%20-filter%3Areplies&src=typed_query'
TWEET_IDENTIFIER = 'div[data-testid="tweet"]'
