# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testManage', '0005_auto_20161031_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testobject',
            name='testLevelTypes',
            field=models.ManyToManyField(to='testManage.LevelType'),
        ),
        migrations.AlterField(
            model_name='testobject',
            name='testLevels',
            field=models.ManyToManyField(to='testManage.Level'),
        ),
    ]