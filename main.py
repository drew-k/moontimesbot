""" Twitter bot that posts the moonrise and moonset times for the day """

import os
import requests
import tweepy
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()  # load environment variables


class Bot():
    """ Setup a twitter bot """
    def __init__(self) -> None:
        self.consumer_key = os.environ.get("CONSUMER_KEY")
        self.consumer_secret = os.environ.get("CONSUMER_SECRET")
        self.access_token = os.environ.get("ACCESS_TOKEN")
        self.access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
        self.api_key = os.environ.get("ASTRONOMY_API_KEY")
        self.client = tweepy.Client(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
            return_type=tweepy.Response
        )

    def astronomy_api_call(self) -> requests.Response:
        return requests.get(f"https://api.ipgeolocation.io/astronomy?apiKey={self.api_key}&location=New%20York,%20US")

    def send_tweet(self, message: str) -> tweepy.Response:
        """ Send a tweet with the given message """
        return self.client.create_tweet(text=message)


def main():
    # Initialize bot
    bot = Bot()

    # Call the astronomy api
    api_response = bot.astronomy_api_call().json()  # Get the response in .json format

    try:
        # Send out the tweet
        if api_response["moon_status"] == "-":
            if api_response["moonrise"] != "-:-" and api_response["moonset"] == "-:-":
                # Get the moonrise time
                unformmated = datetime.strptime(api_response["moonrise"], "%H:%M")  # get datetime object
                moonrise = unformmated.strftime("%I:%M %p")  # convert to 12-hour
                tweet = bot.send_tweet(f"The moon will rise at {moonrise} and not set today in Fort Myers, Florida (EST).")
            elif api_response["moonrise"] == "-:-" and api_response["moonset"] != "-:-":
                # Get the moonset time
                unformmated = datetime.strptime(api_response["moonset"], "%H:%M")  # get datetime object
                moonset = unformmated.strftime("%I:%M %p")  # convert to 12-hour
                tweet = bot.send_tweet(f"The moon will set at {moonset} and not rise today in Fort Myers, Florida (EST).")
            else:
                # Get the moonrise time
                unformmated = datetime.strptime(api_response["moonrise"], "%H:%M")  # get datetime object
                moonrise = unformmated.strftime("%I:%M %p")  # convert to 12-hour
                # Get the moonset time
                unformmated = datetime.strptime(api_response["moonset"], "%H:%M")  # get datetime object
                moonset = unformmated.strftime("%I:%M %p")  # convert to 12-hour

                if api_response["moonrise"] < api_response["moonset"]:
                    tweet = bot.send(f"The moon will rise at {moonrise} and set at {moonset} today in Fort Myers, Florida (EST).")
                else:
                    tweet = bot.send_tweet(f"The moon will set at {moonset} and rise at {moonrise} today in Fort Myers, Florida (EST).")  # normal operation
        else:
            # Get the moonrise time
            unformmated = datetime.strptime(api_response["moonrise"], "%H:%M")  # get datetime object
            moonrise = unformmated.strftime("%I:%M %p")  # convert to 12-hour
            # Get the moonset time
            unformmated = datetime.strptime(api_response["moonset"], "%H:%M")  # get datetime object
            moonset = unformmated.strftime("%I:%M %p")  # convert to 12-hour
            tweet = bot.send_tweet(f"The moon is {api_response['moon_status'].lower()} today in Fort Myers, Florida (EST).")  # if the moon is always up or always set within the day

        print(f"Tweet sent out: https://twitter.com/MoonTimesBot/status/{tweet.data['id']}")
    except tweepy.errors.Forbidden as e:
        print(f"{e}: {e.response.json()['detail']}")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
