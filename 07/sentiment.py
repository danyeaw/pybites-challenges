import json
import sys
from collections import defaultdict

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


def read_json(input_file):
    with open(input_file) as f:
        for line in f.readlines():
            yield json.loads(line)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('please provide json data file')
        sys.exit(1)
    input_file = sys.argv[1]
    tweets = read_json(input_file)
    sentiments = defaultdict(set)
    for tw in tweets:
        tweet_text = dict(tw)['text'].lower()
        blob = TextBlob(tweet_text, analyzer=NaiveBayesAnalyzer())
        sentiments[blob.sentiment.classification].add(tweet_text)

    total = sum(len(i) for i in sentiments.values())

    perc_pos = len(sentiments["pos"]) / total * 100
    perc_neg = len(sentiments["neg"]) / total * 100

    print("Analyzed {} tweets".format(total))
    print("Positive: {:.2f}%".format(perc_pos))
    print("Negative: {:.2f}%".format(perc_neg))
