# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-05 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_tweet'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
