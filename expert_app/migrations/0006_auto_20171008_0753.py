# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-10-08 07:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert_app', '0005_auto_20171007_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system',
            name='slug',
            field=models.CharField(default='', max_length=30, unique=True),
        ),
    ]