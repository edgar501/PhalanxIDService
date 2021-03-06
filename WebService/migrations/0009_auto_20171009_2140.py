# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 21:40
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebService', '0008_auto_20171006_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phalanxiddatamodel',
            name='phalanx_uid',
            field=models.CharField(max_length=64, unique=True, validators=[django.core.validators.RegexValidator('^[A-Fa-fxX0-9\\s]+$', 'Invalid uid. Only hex characters allowed', 'invalid')]),
        ),
    ]
