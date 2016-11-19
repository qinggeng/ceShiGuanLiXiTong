# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 17:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testManage', '0003_auto_20161025_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='testObject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='testManage.TestObject'),
        ),
        migrations.AddField(
            model_name='leveltype',
            name='testObject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='testManage.TestObject'),
        ),
        migrations.AddField(
            model_name='testobject',
            name='description',
            field=models.CharField(default='', max_length=4000),
        ),
        migrations.AddField(
            model_name='testobject',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]