# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testManage', '0006_auto_20161031_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='leveltype',
            name='testObjects',
            field=models.ManyToManyField(to='testManage.TestObject'),
        ),
    ]