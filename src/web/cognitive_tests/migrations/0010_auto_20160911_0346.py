# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-11 00:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cognitive_tests', '0009_auto_20160911_0313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='webtest',
            name='description',
        ),
        migrations.AddField(
            model_name='webtest',
            name='instructions',
            field=models.TextField(blank=True, verbose_name='Инструкция (markdown)'),
        ),
    ]
