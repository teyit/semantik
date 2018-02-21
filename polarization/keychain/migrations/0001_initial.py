# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-19 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consumer_key', models.CharField(max_length=150)),
                ('consumer_key_secret', models.CharField(max_length=150)),
                ('access_token', models.CharField(max_length=150)),
                ('access_token_secret', models.CharField(max_length=150)),
                ('last_used', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
