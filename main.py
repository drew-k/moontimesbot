""" Twitter bot that posts the moonrise and moonset times for the day """

import os
import tweepy
from dotenv import load_dotenv
load_dotenv()  # load the environment variables

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuth1UserHandler(consumer_key,
                                consumer_secret,
                                access_token,
                                access_token_secret)

api = tweepy.API(auth)

for tweet in api.home_timeline():
    print(tweet.text)
