# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-07 11:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_node_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='influencer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='node',
            name='sector',
            field=models.CharField(blank=True, choices=[('alisveris', 'Alışveriş'), ('basin-yayin', 'Basın'), ('dayanikli-tuketim', 'Dayanıklı Tüketim'), ('egitim', 'Eğitim'), ('eglence-yasam', 'Eğlence'), ('enerji', 'Enerji'), ('fenomenler', 'Fenomen'), ('finans', 'Finans'), ('giyim', 'Giyim'), ('hizli-tuketim', 'Hızlı Tüketim'), ('internet', 'İnternet'), ('kamu', 'Kamu'), ('kurumsal', 'Kurumsal'), ('kultur-sanat', 'Kültür Sanat'), ('organizasyon', 'Organizasyon'), ('otomotiv', 'Otomotiv'), ('reklam-pazarlama', 'Reklam'), ('saglik', 'Sağlık'), ('seyahat', 'Seyahat'), ('spor', 'Spor'), ('teknoloji', 'Teknoloji'), ('yapi-sektoru', 'Yapı'), ('diger', 'Diğer')], max_length=100, null=True),
        ),
    ]