import csv
from collections import namedtuple

import mock
import pytest
from tweets import TWEETS  # mock data
from usertweets import UserTweets, NUM_TWEETS

HANDLE = "pybites"
MAX_ID = "819831370113351680"

Tweet = namedtuple("Tweet", ["id_str", "created_at", "text"])


def read_csv(fname):
    with open(fname, encoding="utf-8", newline="") as f:
        has_header = csv.Sniffer().has_header(f.readline())
        f.seek(0)
        r = csv.reader(f)
        if has_header:
            next(r, None)  # skip the header
        return [Tweet(*tw) for tw in r]  # list(r)


@pytest.fixture(scope="module")
def user():
    with mock.patch("tweepy.API.user_timeline") as mock_timeline:
        mock_timeline.return_value = TWEETS
        user_tweets = UserTweets(HANDLE, max_id=MAX_ID)
        return user_tweets


def test_num_tweets(user):
    assert len(user) == NUM_TWEETS


def test_first_tweet_returned_by_api(user):
    tw_n = 0
    assert user[tw_n].id_str == MAX_ID
    assert user[tw_n].created_at == TWEETS[tw_n].created_at
    assert user[tw_n].text == TWEETS[tw_n].text


def test_read_back_from_cached_csv(user):
    csv_tweets = read_csv(user.output_file)
    assert len(csv_tweets) == NUM_TWEETS
    tw_n = 0  # first
    assert csv_tweets[tw_n].id_str == MAX_ID
    assert csv_tweets[tw_n].created_at == str(TWEETS[tw_n].created_at)
    assert csv_tweets[tw_n].text == TWEETS[tw_n].text
    tw_n = -1  # last
    assert csv_tweets[tw_n].text == TWEETS[tw_n].text
