# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 22:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebService', '0002_auto_20170922_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phalanxiddatamodel',
            name='phalanx_uid',
            field=models.CharField(max_length=10),
        ),
    ]
