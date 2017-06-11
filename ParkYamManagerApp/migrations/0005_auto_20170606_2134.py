# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-06 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParkYamManagerApp', '0004_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='reply_time',
        ),
        migrations.AlterField(
            model_name='message',
            name='replier_name',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Replier'),
        ),
        migrations.AlterField(
            model_name='message',
            name='reply',
            field=models.TextField(blank=True, default='', verbose_name='Reply'),
        ),
    ]
