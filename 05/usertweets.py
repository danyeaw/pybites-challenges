from collections import namedtuple
import csv
import os

import tweepy

from config_nogit import CONSUMER_KEY, CONSUMER_SECRET
from config_nogit import ACCESS_TOKEN, ACCESS_SECRET

DEST_DIR = "data"
EXT = "csv"
NUM_TWEETS = 200

Tweet = namedtuple("Tweet", "id_str created_at text")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
API = tweepy.API(auth)


class UserTweets(object):
    def __init__(self, handle, max_id=None):
        """Get handle and optional max_id.
        Use tweepy.OAuthHandler, set_access_token and tweepy.API
        to create api interface.
        Use _get_tweets() helper to get a list of tweets.
        Save the tweets as data/<handle>.csv"""
        self.handle = handle
        self.max_id = max_id
        self.output_file = f"{os.path.join(DEST_DIR, self.handle)}.{EXT}"
        self._tweets = list(self._get_tweets())
        self._save_tweets()

    def _get_tweets(self):
        """Hint: use the user_timeline() method on the api you defined in init.
        See tweepy API reference: http://docs.tweepy.org/en/v3.5.0/api.html
        Use a list comprehension / generator to filter out fields
        id_str created_at text (optionally use namedtuple)"""
        tweets = API.user_timeline(self.handle, max_id=self.max_id, count=NUM_TWEETS)
        return (
            Tweet(tweet.id_str, tweet.created_at, tweet.text.replace("\n", ""))
            for tweet in tweets
        )

    def _save_tweets(self):
        """Use the csv module (csv.writer) to write out the tweets.
        If you use a namedtuple get the column names with Tweet._fields.
        Otherwise define them as: id_str created_at text
        You can use writerow for the header, writerows for the rows"""
        with open(self.output_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(Tweet._fields)
            writer.writerows(self._tweets)

    def __len__(self):
        """See http://pybit.es/python-data-model.html"""
        return len(self._tweets)

    def __getitem__(self, pos):
        """See http://pybit.es/python-data-model.html"""
        return self._tweets[pos]


if __name__ == "__main__":

    handles = """pybites danyeaw bbelderbos importpython lifehacker 
    jsonmez Schwarzenegger github treyhunner
    raymondh gvanrossum dbader_org newsafaribooks tferriss""".split()

    for handle in handles:
        print("--- {} ---".format(handle))
        user = UserTweets(handle)
        for tw in user[:5]:
            print(tw)
        print()
