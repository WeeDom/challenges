from collections import namedtuple
import csv
import os
import tweepy
from config import CONSUMER_KEY, CONSUMER_SECRET
from config import ACCESS_TOKEN, ACCESS_SECRET

DEST_DIR = 'data'
EXT = 'csv'
NUM_TWEETS = 100

Tweet = namedtuple('Tweet', 'id_str created_at text')


class UserTweets(object):

    def __init__(self, handle, max_id=None):
        auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.apply_auth()
        self.api = tweepy.API(auth)
        self.handle = handle
        self._tweets = list(self._get_tweets())
        self._save_tweets()

    def _get_tweets(self):
        tweetstup  = namedtuple('Tweet', 'id_str time text')
        tweetsarray = []
        for status in self.api.user_timeline(handle, count=NUM_TWEETS):
            tup = tweetstup(status.id_str, status.created_at, status.text)
            tweetsarray.append(tup)

        return tweetsarray


    def _save_tweets(self):
        with open(DEST_DIR + '/tweets.'+ EXT, mode='a+') as tweets_file:
            fnames = self._tweets[0]._fields
            writer = csv.DictWriter(tweets_file, fieldnames=fnames)
            writer.writeheader()
            for tup in self._tweets:
                writer.writerow({"id_str":tup.id_str, "time": tup.time, "text": tup.text})

        return True

    def __len__(self):
        return len(self._tweets)

    def __getitem__(self, pos):
        return self._tweets[pos]


if __name__ == "__main__":
    if os.path.exists(DEST_DIR + '/tweets.' + EXT):
        os.remove(DEST_DIR + '/tweets.' + EXT)
    for handle in ('pybites', 'bbelderbos', 'wee_dom'):
        print('--- {} ---'.format(handle))
        user = UserTweets(handle)
        for tw in user[:5]:
            print(tw)
        print()
