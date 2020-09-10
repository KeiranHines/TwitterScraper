import argparse
import logging
import sched
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

import flask
from flask import abort

from src.framework import AbstractScraper
from src.handlers import CollectorHandler
from src.twitter import TwitterScraper

app = flask.Flask(__name__)
userHandlers: Dict[str, CollectorHandler] = dict()


def run_on_schedule(sc, seconds, scrapper: AbstractScraper):
    """Runs the scrapper update on a given interval.
    :param sc: scheduler - The scheduler to use to refresh.
    :param seconds: int - The frequency in seconds to  update the tweets.
    :param scrapper: IScraper - The scraper to update each tick.
    :return: None
    """
    scrapper.update()
    sc.enter(seconds, 1, run_on_schedule, (sc, seconds, scrapper))


def setup_web_server(debug: bool):
    app.config["DEBUG"] = debug  # Command line arg this.


@app.route('/', methods=['GET'])
def home():
    """ Landing page route. """
    user_list = '<ul>'
    for key in userHandlers.keys():
        user_list += str.format('<li>{user}</li>', user=key)
    user_list += '<ul>'
    # Improvement: make this a template and a nicer page
    return "<h1>Tweet Scraper home</h1><p>tweets are available at /user/<user></p><h3>Configured Users:</h3>" + user_list


@app.route('/user/<user>', methods=['GET'])
def get_tweets(user: str):
    """ Route to access users tweets. """
    if user in userHandlers:
        return userHandlers.get(user).as_json()
    # Improvement custom 404 if the was web accessed.
    abort(404)


def _setup_args():
    """ Sets up command line args. """
    logging.basicConfig(format='%(asctime)s[%(levelname)s]:%(message)s')
    parser = argparse.ArgumentParser(prog='TweetLogger', description='Command line twitter feed for a user')
    req = parser.add_argument_group('required arguments')
    req.add_argument('-u', '--users', type=str, nargs='+', help='The user to follow', required=True)
    parser.add_argument('-i', '--initial', type=int, default='5', help='Initial tweets to load (>= 0)')
    parser.add_argument('-p', '--port', type=int, default='5000', help='webserver port (0 to 65353)')
    parser.add_argument('-r', '--refresh', type=int, default='10', help='Refresh interval (minutes > 0)')

    return vars(parser.parse_args())


if __name__ == '__main__':
    args = _setup_args()
    initial = args['initial']
    if initial < 0:
        raise argparse.ArgumentTypeError("Initial is less than 0")
    minutes = args['refresh']
    if minutes <= 0:
        raise argparse.ArgumentTypeError("Refresh period is less that every minute")
    port = args['port']
    if port < 0 or port > 65353:
        raise argparse.ArgumentTypeError("Invalid port")
    s = minutes * 60

    setup_web_server(True)
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.run(blocking=False)

    # No max-workers specified, using CPU thread count for proof of concept
    with ThreadPoolExecutor() as executor:
        for user in args['users']:
            if user not in userHandlers:
                tweetScraper = TwitterScraper(target=user)
                handler = CollectorHandler()
                userHandlers[user] = handler
                tweetScraper.register_handler(handler)
                logging.debug("Started tweet scraper for %s, initial load: %d, refreshing every %d minutes", user,
                              initial, minutes)
                executor.submit(tweetScraper.get_latest, count=initial)
                scheduler.enter(s, 1, run_on_schedule, (scheduler, s, tweetScraper))
            else:
                logging.info("User %s already loaded", user)
        app.run(use_reloader=False, port=port)
