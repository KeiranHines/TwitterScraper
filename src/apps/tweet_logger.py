import argparse
import logging
import sched
import time

from src.framework import AbstractScraper
from src.handlers import StdOutHandler
from src.twitter import TwitterScraper


def run_on_schedule(sc, seconds, scrapper: AbstractScraper):
    """Runs the scrapper update on a given interval.
    :param sc: scheduler - The scheduler to use to refresh.
    :param seconds: int - The frequency in seconds to  update the tweets.
    :param scrapper: IScraper - The scraper to update each tick.
    :return: None
    """
    scrapper.update()
    sc.enter(seconds, 1, run_on_schedule, (sc, seconds, scrapper))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='TweetLogger', description='Command line twitter feed for a user')
    req = parser.add_argument_group('required arguments')
    req.add_argument('-u', '--user', type=str, help='The user to follow', required=True)
    parser.add_argument('-i', '--initial', type=int, default='5', help='Initial tweets to load (>= 0)', )
    parser.add_argument('-r', '--refresh', type=int, default='10', help='Refresh interval (minutes > 0)')

    args = vars(parser.parse_args())
    initial = args['initial']
    if initial < 0:
        raise argparse.ArgumentTypeError("Initial is less than 0")
    minutes = args['refresh']
    if minutes <= 0:
        raise argparse.ArgumentTypeError("Refresh period is less that every minute")
    user = args['user']
    s = minutes * 60

    logging.basicConfig(format='%(asctime)s[%(levelname)s]:%(message)s')
    scheduler = sched.scheduler(time.time, time.sleep)
    tweetScraper = TwitterScraper(target=user)
    tweetScraper.register_handler(StdOutHandler())
    logging.debug("Started tweet scraper for %s, initial load: %d, refreshing every %d minutes", user, initial, minutes)
    tweetScraper.get_latest(count=initial)
    scheduler.enter(s, 1, run_on_schedule, (scheduler, s, tweetScraper))
    scheduler.run()
