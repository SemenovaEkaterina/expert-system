# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-10-08 10:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('expert_app', '0006_auto_20171008_0753'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeAllowedValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(max_length=50)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ObjectAttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='attributevalue',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='objectattributes',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='objectattributes',
            name='object',
        ),
        migrations.RemoveField(
            model_name='objectattrvalues',
            name='attr_value',
        ),
        migrations.RemoveField(
            model_name='objectattrvalues',
            name='object',
        ),
        migrations.AlterModelManagers(
            name='question',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='answer',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='compare',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='parameter',
        ),
        migrations.RemoveField(
            model_name='question',
            name='text',
        ),
        migrations.AddField(
            model_name='answer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='answer',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='answer',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='attribute',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attribute',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='attribute',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='object',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='object',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='object',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='parameter',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parameter',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='parameter',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='parameter',
            name='type',
            field=models.IntegerField(choices=[(0, 'Заранее определенные значения'), (1, 'Любые значения')], default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametervalue',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='parametervalue',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='parametervalue',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='question',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='parameter',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='expert_app.Parameter'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rule',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rule',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='rule',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='system',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='system',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='expert_app.System'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='object',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='object',
            name='system',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='expert_app.System'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='parameter',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='system',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='expert_app.System'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='parametervalue',
            name='value',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='question',
            name='system',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='expert_app.System'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.IntegerField(choices=[(0, 'Заранее определенные значения'), (1, 'Число'), (2, 'Строка')]),
        ),
        migrations.DeleteModel(
            name='AttributeValue',
        ),
        migrations.DeleteModel(
            name='ObjectAttributes',
        ),
        migrations.DeleteModel(
            name='ObjectAttrValues',
        ),
        migrations.AddField(
            model_name='objectattributevalue',
            name='attribute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert_app.Attribute'),
        ),
        migrations.AddField(
            model_name='objectattributevalue',
            name='attribute_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert_app.AttributeAllowedValue'),
        ),
        migrations.AddField(
            model_name='objectattributevalue',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert_app.Object'),
        ),
        migrations.AddField(
            model_name='attributeallowedvalue',
            name='attribute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expert_app.Attribute'),
        ),
    ]