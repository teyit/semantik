# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-23 09:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommonFollowers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_followers', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=255)),
                ('followers', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='follower',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Node'),
        ),
        migrations.AddField(
            model_name='commonfollowers',
            name='first_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Node'),
        ),
        migrations.AddField(
            model_name='commonfollowers',
            name='second_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='second_node', to='accounts.Node'),
        ),
    ]