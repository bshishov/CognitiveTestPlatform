# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-09 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cognitive_tests', '0005_auto_20170109_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveymark',
            name='max_value',
            field=models.IntegerField(blank=True, null=True, verbose_name='max value'),
        ),
        migrations.AddField(
            model_name='surveymark',
            name='min_value',
            field=models.IntegerField(blank=True, null=True, verbose_name='min value'),
        ),
        migrations.AddField(
            model_name='testmark',
            name='max_value',
            field=models.IntegerField(blank=True, null=True, verbose_name='max value'),
        ),
        migrations.AddField(
            model_name='testmark',
            name='min_value',
            field=models.IntegerField(blank=True, null=True, verbose_name='min value'),
        ),
    ]