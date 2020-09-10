# Proof of concept web scraper

## Directory Structure
<pre>
src: All source
|
|-->apps: Apps based on these scrapers.
|
|-->framework: The framework for this an future web-scrapers.
        |
        |-->exceptions: Exception handling for the framework. 
|
|-->handlers: Handlers that process AbstactDataClass data
|
|-->twitter: A Twitter specific user scraper
</pre>

### Usages ###
* apps/tweet_logger.py
    * Description: gets the last I tweets for a given twitter handle and logs to stdout, updating every M minutes
    * Usage: tweet_logger.py -u <user> -i <initial> -m <Minutes>
    * Defaults:
        * If -i is not specified default to 5.
        * If -m is not specified default to 10.
* apps/rest_api.py
    * Description: A simple webserver that will provide an update of users tweets, updating every M minutes
    * Usage: tweet_logger.py -u <users> -i <initial> -m <Minutes>
    * Multiple users can be specified with -u <user1> <user2> 
    * Defaults:
        * If -i is not specified default to 5.
        * If -m is not specified default to 10.
    