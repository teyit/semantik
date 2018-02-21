import sys
import os
import time

import tweepy
import django

from polarization.secrets import PROJECT_PATH

sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = "polarization.settings"
django.setup()

from polarization.keychain.models import Key
from polarization.search.models import Tweet, Search

key = Key.objects.filter(stream=True).first()
auth = tweepy.OAuthHandler(consumer_key=key.consumer_key, consumer_secret=key.consumer_key_secret)
auth.set_access_token(key.access_token, key.access_token_secret)
api = tweepy.API(auth)

keywords = list(Search.objects.filter().values_list("keyword", flat=True))


class Listener(tweepy.StreamListener):

    def on_status(self, status):
        status_json = status._json
        if not "retweeted_status" in status_json:
            for keyword in keywords:
                if keyword in status_json["text"]:
                    Tweet.objects.create(
                        search=Search.objects.get(keyword=keyword),
                        in_reply_to=status_json["in_reply_to_screen_name"],
                        username=status_json['user']['screen_name'],
                        followers=status_json['user']['followers_count'],
                        retweets=status_json['retweet_count'],
                        favorites=status_json['favorite_count'],
                        text=status_json['text'],
                        date_created=status.created_at
                    )
        else:
            pass


listener = Listener()
stream = tweepy.Stream(auth=api.auth, listener=listener)
stream.filter(track=keywords, async=True, languages=['tr'])

while True:
    new_keywords = Search.objects.filter(active=True)
    for keyword in new_keywords:
        if not keyword.is_active:
            keyword.active = False
            keyword.save()
    new_keywords = list(Search.objects.filter(active=True).values_list("keyword", flat=True))
    if new_keywords == keywords:
        time.sleep(30)
        continue
    else:
        keywords = new_keywords
        if stream.running:
            stream.disconnect()
            del stream
        if keywords == []:
            continue
        else:
            stream = tweepy.Stream(auth=api.auth, listener=listener)
            stream.filter(track=keywords, async=True, languages=['tr'])
        time.sleep(30)  # Refresh keywords in every thirty seconds
