from django.contrib import admin

from .models import Node, Follower, CommonFollowers

admin.site.register(Node)
admin.site.register(Follower)
admin.site.register(CommonFollowers)
