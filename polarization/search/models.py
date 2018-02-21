from django.db import models
from django.utils import timezone
from background_task import background
from social_django.models import UserSocialAuth
import tweepy
import time

from polarization.keychain.models import Key
from polarization.accounts.constants import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from .constants import LANGUAGE_CHOICES


class Search(models.Model):
    keyword = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    finish_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=7))
    created_by = models.ForeignKey(UserSocialAuth, null=True, blank=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Search, self).save(*args, **kwargs)
        if created:
            Key.objects.get_or_create(
                consumer_key=TWITTER_CONSUMER_KEY,
                consumer_key_secret=TWITTER_CONSUMER_SECRET,
                access_token=self.created_by.extra_data['access_token']['oauth_token'],
                access_token_secret=self.created_by.extra_data['access_token']['oauth_token_secret']
            )
            get_tweets(self.keyword, self.language, self.start_date.isoformat())

    @property
    def is_active(self):
        return self.finish_date > timezone.now()

    def __str__(self):
        return self.keyword


class Tweet(models.Model):
    search = models.ForeignKey(Search)
    in_reply_to = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField()
    text = models.TextField()
    username = models.CharField(max_length=100)
    followers = models.PositiveIntegerField()
    retweets = models.PositiveIntegerField()
    favorites = models.PositiveIntegerField()

    def __str__(self):
        return self.text + " - " + self.search.keyword


@background(queue="tweet")
def get_tweets(keyword, language, start_date=None, finish_date=None):
    if start_date is not None:
        # TODO: Make it better
        start_date = timezone.datetime.strptime(start_date[:-13], '%Y-%m-%dT%H:%M:%S')
    auths = []
    auth_index = 0
    keys = Key.objects.filter(stream=False)
    for key in keys:
        auth = tweepy.OAuthHandler(key.consumer_key, key.consumer_key_secret)
        auth.set_access_token(key.access_token, key.access_token_secret)
        auths.append(auth)
    api = tweepy.API(auths[0])

    swap_factor = (60 / len(auths)) + 1

    def handle_limit(cursor):
        global auth_index
        while True:
            try:
                yield cursor.next()
                time.sleep(swap_factor)
            except tweepy.RateLimitError:
                if auth_index == len(auths) - 1:
                    auth_index = 0
                else:
                    auth_index += 1
                    eligible_key = True
                    while eligible_key:
                        if keys[auth_index].is_usable():
                            keys[auth_index].last_used = timezone.now()
                            keys[auth_index].save()
                            eligible_key = False
                        else:
                            auth_index += 1
                api.auth = auths[auth_index]

    for page in handle_limit(tweepy.Cursor(api.search, q='"' + keyword + '"', count=1000, lang=language).pages()):
        search = Search.objects.get(keyword=keyword)
        for tweet in page:
            if not "retweeted_status" in tweet._json and tweet.created_at > start_date:
                Tweet.objects.create(
                    search=search,
                    in_reply_to=tweet._json['in_reply_to_screen_name'],
                    username=tweet._json['user']['screen_name'],
                    followers=tweet._json['user']['followers_count'],
                    retweets=tweet._json['retweet_count'],
                    favorites=tweet._json['favorite_count'],
                    text=tweet._json['text'],
                    date_created=tweet.created_at
                )
            else:
                pass
