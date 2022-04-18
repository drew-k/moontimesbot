""" Twitter bot that posts the moonrise and moonset times for the day """

import os
import configparser
import tweepy
from dotenv import load_dotenv
load_dotenv()  # load the environment variables

class Bot():
    """ Setup a twitter bot """
    def __init__(self):
        self.consumer_key = os.environ.get("CONSUMER_KEY")
        self.consumer_secret = os.environ.get("CONSUMER_SECRET")
        self.access_token = os.environ.get("ACCESS_TOKEN")
        self.access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
        self.client = tweepy.Client(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )

    def send_tweet(self, message: str):
        """ Send a tweet with the given message """
        return self.client.create_tweet(text=message)

# Initialize bot
bot = Bot()

tweet = bot.send_tweet("Test message from python")
print(f"https://twitter.com/user/status/{tweet.data['id']}")

