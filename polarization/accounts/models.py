import time

from django.db import models
from django.utils import timezone
from background_task import background
import tweepy
from social_django.models import UserSocialAuth

from polarization.keychain.models import Key
from .constants import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, INFLUENCER_SECTOR_CHOICES


class Node(models.Model):
    handle = models.CharField(max_length=255)
    created_by = models.ForeignKey(UserSocialAuth, null=True, blank=True)
    status = models.BooleanField(default=False)  # False = In Progress, True = Finished
    followers = models.PositiveIntegerField(default=0)
    influencer = models.BooleanField(default=False)
    sector = models.CharField(max_length=100, null=True, blank=True, choices=INFLUENCER_SECTOR_CHOICES)

    def __str__(self):
        return self.handle

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(Node, self).save(*args, **kwargs)
        if created:
            Key.objects.get_or_create(
                consumer_key=TWITTER_CONSUMER_KEY,
                consumer_key_secret=TWITTER_CONSUMER_SECRET,
                access_token=self.created_by.extra_data['access_token']['oauth_token'],
                access_token_secret=self.created_by.extra_data['access_token']['oauth_token_secret']
            )
            get_followers(self.handle)


class Follower(models.Model):
    node = models.ForeignKey(Node)
    twitter_id = models.CharField(max_length=255)

    def __str__(self):
        return self.twitter_id


class CommonFollowers(models.Model):
    first_node = models.ForeignKey(Node)
    second_node = models.ForeignKey(Node, related_name="second_node")
    common_followers = models.PositiveIntegerField(default=0)

    @property
    def graph_factor(self):
        first_node_followers = self.first_node.followers
        second_node_followers = self.first_node.followers
        if first_node_followers > second_node_followers:
            return self.common_followers / second_node_followers
        else:
            return self.common_followers / first_node_followers


@background(queue='follower')
def get_followers(screen_name):
    auths = []
    auth_index = 0
    keys = Key.objects.filter(stream=False)
    for key in keys:
        auth = tweepy.OAuthHandler(key.consumer_key, key.consumer_key_secret)
        auth.set_access_token(key.access_token, key.access_token_secret)
        auths.append(auth)
    api = tweepy.API(auths[0])
    auths[0].last_used = timezone.now()
    auths[0].save()

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

    node = Node.objects.get(handle=screen_name)
    for page in handle_limit(tweepy.Cursor(api.followers_ids, screen_name=screen_name, lang='tr').pages()):
        for twitter_id in page:
            common_nodes = Follower.objects.filter(twitter_id=twitter_id)
            if common_nodes.exists():
                for common_node in common_nodes:
                    common_obj, created = CommonFollowers.objects.get_or_create(first_node=node, second_node=common_node.node)
                    common_obj.common_followers += 1
                    common_obj.save()
            Follower.objects.create(node=node, twitter_id=twitter_id)

    node.followers = Follower.objects.filter(node=node).count()
    node.save()
