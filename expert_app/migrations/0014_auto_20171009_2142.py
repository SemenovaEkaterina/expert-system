# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-10-09 18:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert_app', '0013_auto_20171009_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='parameter_value_any',
            field=models.CharField(default='', max_length=50, null=True),
        ),
    ]
