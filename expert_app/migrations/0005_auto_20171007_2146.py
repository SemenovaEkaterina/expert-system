# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-10-07 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert_app', '0004_auto_20171007_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system',
            name='slug',
            field=models.CharField(default='', max_length=30),
        ),
    ]