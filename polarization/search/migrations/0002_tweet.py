# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-01 08:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_reply_to', models.CharField(blank=True, max_length=100, null=True)),
                ('date_created', models.DateTimeField()),
                ('text', models.TextField()),
                ('username', models.CharField(max_length=100)),
                ('followers', models.PositiveIntegerField()),
                ('retweets', models.PositiveIntegerField()),
                ('favorites', models.PositiveIntegerField()),
                ('search', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.Search')),
            ],
        ),
    ]
