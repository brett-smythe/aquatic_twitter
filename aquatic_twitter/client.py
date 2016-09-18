"""Twitter client for aquatic services"""
# pylint: disable=import-error
from functools import wraps

import twitter


class AquaticTwitter(object):
    """Class for interating with twitter API"""
    # pylint: disable=too-many-arguments
    def __init__(self, consumer_key, consumer_secret,
                 access_token_key, access_token_secret,
                 write_to_memcache=False):

        self.client = twitter.Api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token_key,
            access_token_secret=access_token_secret
        )
        self.client.InitializeRateLimit()

        self.base_rate_limit_url = (
            'https://api.twitter.com/1.1/application/'
            'rate_limit_status.json?resources={0}'
        )

    def _handle_twitter_errors(func):
        """
        Handles hitting the twitter API ratelimit
        """
        # pylint: disable=missing-docstring
        @wraps(func)
        def func_wrapper(self, *args, **kwargs):
            ret_val = None
            try:
                ret_val = func(self, *args, **kwargs)
            except twitter.TwitterError as e:
                if 'Exceeded connection limit for user' in e.message:
                    # TODO do something with this
                    pass
                elif 'Capacity Error' in e.message:
                    # TODO do something with this
                    pass
                elif 'Technical Error' in e.message:
                    # TODO do something with this
                    pass

            return ret_val

        return func_wrapper

    @_handle_twitter_errors
    def get_timeline_tweets(self, screen_name):
        """
        Pulls the max number of tweets from a twitter user's timeline with
        screen_name where screen_name is the string following the @ symbol
        in the user's name.
        """
        timeline_tweets = self.client.GetUserTimeline(
            screen_name=screen_name, count=200
        )
        return timeline_tweets

    @_handle_twitter_errors
    def get_timeline_tweets_since_id(self, screen_name, since_id):
        """
        Pulls the max number of tweets from a twitter user's timeline up to the
        tweet with the tweet id of since_id with screen_name where screen_name
        is the string following the @ symbol in the user's name.
        """
        timeline_tweets = self.client.GetUserTimeline(
            screen_name=screen_name, count=200, since_id=since_id
        )
        return timeline_tweets

    def get_user_timeline_rate_limit(self):
        """
        Make a request to the twitter API to get the current rate limit status
        for the endpoint of '/statuses/user_timeline'
        """
        user_tl_rate_url = self.base_rate_limit_url.format(
            'statuses,search'
        )
        rate_limit_data = self.client.CheckRateLimit(
            user_tl_rate_url
        )
        return rate_limit_data
