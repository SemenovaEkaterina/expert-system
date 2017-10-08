# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-10-08 10:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert_app', '0007_auto_20171008_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='type',
            field=models.IntegerField(choices=[(0, 'Заранее определенные значения'), (1, 'Любые значения')], default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.IntegerField(choices=[(0, 'Заранее определенные значения'), (1, 'Число'), (2, 'Строка')], default=0),
        ),
    ]
