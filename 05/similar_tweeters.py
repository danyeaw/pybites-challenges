import csv
import re
import sys

import nltk
from gensim import corpora, models, similarities

nltk.download("stopwords")
STOPWORDS = set(nltk.corpus.stopwords.words("english"))
IS_LINK_OBJ = re.compile(r'^(?:@|https?://)')


def _is_ascii(word):
    return len(word) == len(word.encode())


def tokenize_text(words):
    words = [word for word in words if len(word) > 4 and word not in STOPWORDS]
    words = [word for word in words if _is_ascii(word)]
    words = [word for word in words if not IS_LINK_OBJ.search(word)]
    return words


def get_user_tokens(user):
    tweets_csv = f"data/{user}.csv"
    words = []
    with open(tweets_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for w in row['text'].lower().split():
                words.append(w)
    return tokenize_text(words)


def similar_tweeters(user1, user2):
    tokens = get_user_tokens(user1)
    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(tokens)]
    lda = models.LdaModel(corpus, num_topics=5, id2word=dictionary, passes=15)
    index = similarities.MatrixSimilarity(lda[corpus])

    tokens = get_user_tokens(user2)
    vec_bow = dictionary.doc2bow(tokens)
    vec_lda = lda[vec_bow]

    sims = index[vec_lda]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    for i, sim in sims:
        print(user2, sim)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: {} <user1> <user2>'.format(sys.argv[0]))
        sys.exit(1)

    user1, user2 = sys.argv[1:3]
    similar_tweeters(user1, user2)
