# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-18 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebService', '0013_phalanxiddatamodel_phalanx_ok'),
    ]

    operations = [
        migrations.AddField(
            model_name='phalanxiddatamodel',
            name='firmware_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='phalanxiddatamodel',
            name='firmware_version',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
