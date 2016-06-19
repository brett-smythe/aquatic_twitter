import sys, traceback
from functools import wraps

import twitter
from pymemcache.client.base import Client as MemCacheClient
from pymemcache.exceptions import ( MemcacheServerError,
    MemcacheUnexpectedCloseError
)

from settings import aquatic_settings


class AquaticTwitter(object):

    # Add a client to log things
    def __init__(self, consumer_key, consumer_secret,
        access_token_key, access_token_secret, write_to_memcache=False):
        
        self.client = twitter.Api(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=access_token_key,
            access_token_secret=access_token_secret
        )
        self.client.InitializeRateLimit()

        self.base_rate_limit_url= (
            'https://api.twitter.com/1.1/application/'
            'rate_limit_status.json?resources={0}'
        )

        self.write_to_memcache = write_to_memcache
        self.memcacheClient = None
        if self.write_to_memcache is True:
            self.memcacheClient = MemCacheClient(
                (
                    aquatic_settings.memcache_host,
                    aquatic_settings.memcache_port
                )
            )

    def _handle_twitter_errors(func):
        """
        Handles hitting the twitter API ratelimit
        """
        @wraps(func)
        def func_wrapper(self, *args, **kwargs):
            try:
                ret_val = func(self, *args, **kwargs)
            except twitter.TwitterError as e:
                if 'Exceeded connection limit for user' in e.message:
                    # TODO log this
                    print 'Exceeded twitter API limits'
                    if self.write_to_memcache:
                        self.memcacheClient.set(
                            'over_twitter_api_limits', True
                        )
                elif 'Capacity Error' in e.message:
                    # TODO log this
                    if self.write_to_memcache:
                        self.memcacheClient.set(
                            'twitter_api_error', True
                        )
                elif 'Technical Error' in e.message:
                    # TODO log this
                    if self.write_to_memcache:
                        self.memcacheClient.set(
                            'twitter_api_error', True
                        )
            except MemcacheServerError as e:
                print(e)
                # TODO log this

            except MemcacheUnexpectedCloseError as e:
                print(e)
                # TODO log this

            return ret_val

        return func_wrapper

    def _update_memcache_limits(func):
        """
        Wrapper for updating memcache with twitter limits data
        """
        @wraps(func)
        def func_wrapper(self, *args, **kwargs):
            try:
                ret_val = func(self, *args, **kwargs)

                if self.write_to_memcache:
                    self.user_tl_resources = (
                        self.client.rate_limit.resources['statuses']
                        ['/statuses/user_timeline']
                    )

                    timeline_remaining = self.user_tl_resources['remaining']
                    timeline_reset_time = self.user_tl_resources['reset']
                    timeline_limit = self.user_tl_resources['limit']

                    self.memcacheClient.set(
                        'timeline_remaining', timeline_remaining
                    )
                    self.memcacheClient.set(
                        'timeline_reset', timeline_reset_time
                    )
                    self.memcacheClient.set('timeline_limit', timeline_limit)
            except MemcacheServerError as e:
                print(e)
                # TODO log this
                pass

            except MemcacheUnexpectedCloseError as e:
                print(e)
                # TODO log this
                pass
            return ret_val
        return func_wrapper

    @_handle_twitter_errors
    @_update_memcache_limits
    def get_timeline_tweets(self, screen_name):
        """
        Pulls the max number of tweets from a twitter user's timeline with
        screen_name where screen_name is the string following the @ symbol
        in the user's name.
        """
        self.timeline_tweets = self.client.GetUserTimeline(
            screen_name=screen_name, count=200
        )
        print 'Get timeline!'
        return self.timeline_tweets

    @_update_memcache_limits
    def get_timeline_tweets_since_id(self, screen_name, since_id):
        """
        Pulls the max number of tweets from a twitter user's timeline up to the
        tweet with the tweet id of since_id with screen_name where screen_name
        is the string following the @ symbol in the user's name.
        """
        self.timeline_tweets = self.client.GetUserTimeline(
            screen_name=screen_name, count=200, since_id=since_id
        )
        return self.timeline_tweets

    def get_user_timeline_rate_limit(self):
        """
        Make a request to the twitter API to get the current rate limit status
        for the endpoint of '/statuses/user_timeline'
        """
        self.user_tl_rate_url = self.base_rate_limit_url.format('statuses,search')
        self.rate_limit_data = self.client.CheckRateLimit(
            self.user_tl_rate_url
        )
        return self.rate_limit_data

