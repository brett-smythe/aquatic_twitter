"""Tests for aquatic_twitter client"""
# pylint: disable=import-error
import unittest

import mock

from aquatic_twitter import client as aquatic_client


class TwitterClientCases(unittest.TestCase):
    """Class to test aquatic twitter client"""
    # pylint: disable=too-many-public-methods
    screen_name = 'MalcomReynolds'

    def get_aquatic_twitter_client(self):
        """Create a test aquatic twitter client"""
        # pylint: disable=no-self-use
        test_client = aquatic_client.AquaticTwitter(
            'fake_consumer_key',
            'fake_consumer_secret',
            'fake_token_key',
            'fake_access_token'
        )
        return test_client

    @mock.patch('twitter.Api')
    def test_get_timeline_tweets(self, mocked_twitter):
        """Test get max twitter user timeline tweets"""
        # pylint: disable=unused-argument
        twitter_client = self.get_aquatic_twitter_client()
        twitter_client.get_timeline_tweets(self.screen_name)
        twitter_client.client.GetUserTimeline.assert_called_with(
            screen_name=self.screen_name,
            count=200
        )

    @mock.patch('twitter.Api')
    def test_get_timeline_tweet_since_ids(self, mocked_twitter):
        """Test get max twitter user timeline tweets"""
        # pylint: disable=unused-argument
        since_id = '42'
        twitter_client = self.get_aquatic_twitter_client()
        twitter_client.get_timeline_tweets_since_id(self.screen_name, since_id)
        twitter_client.client.GetUserTimeline.assert_called_with(
            screen_name=self.screen_name,
            count=200,
            since_id=since_id
        )

    @mock.patch('twitter.Api')
    def test_get_user_timeline_rate_limit(self, mocked_twitter):
        """Test get max twitter user timeline tweets"""
        # pylint: disable=unused-argument
        twitter_client = self.get_aquatic_twitter_client()
        twitter_client.get_user_timeline_rate_limit()
        ratelimit_url = twitter_client.base_rate_limit_url.format(
            'statuses,search'
        )
        twitter_client.client.CheckRateLimit.assert_called_with(
            ratelimit_url
        )
