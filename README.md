# Aquatic Twitter

Wrapper for interns-twitter around [python-twitter](https://github.com/bear/python-twitter)

To see how this fits in with the other repos please see [Aquatic Services Wiki](https://github.com/brett-smythe/ansible_configs/wiki)

## Install
```
python setup.py install
```

### External Dependencies
* Network access to twitter's API
* Single-user [Twitter OAuth](https://dev.twitter.com/oauth/overview/single-user) 

## Usage
Both of the below return lists of a [Status Model](https://github.com/bear/python-twitter/blob/53ac36bc2d6a7b4f9ebc838de92a5089318aaacd/twitter/models.py#L370)
```
from aquatic_twitter import client
twitterClient = client.AquaticTwitter(
    twitter_consumer_key,
    twitter_consumer_secret,
    twitter_access_token_key,
    twitter_access_token_secret
)

# Returns the maximum number of timeline tweets (200) you can pull for a user
twitterClient.get_timeline_tweets('twitter_screen_name')

# Returns the maximum number of timeline tweets (200) you pull for a user up to tweet_id
statuses = twitterClient.get_timeline_tweets('twitter_screen_name', last_retrieved_tweet_id)

# Some example attributes

first_status = statuses[0]

first_status.text
>"This would be the tweet text you would see"

first_status.id_str
>"<tweet_id_as_you_would_use_above>"

first_status.screen_name
>"twitter_screen_name"
```
