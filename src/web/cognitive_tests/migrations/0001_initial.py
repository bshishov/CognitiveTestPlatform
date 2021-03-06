# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-24 02:16
from __future__ import unicode_literals

import cognitive_tests.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import sorl.thumbnail.fields
import sortedm2m.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('info', jsonfield.fields.JSONField(verbose_name='information')),
                ('path', models.FilePathField(allow_files=False, allow_folders=True, path='C:\\Users\\boris\\Documents\\CognitiveTestPlatform\\src\\web\\modules', verbose_name='path')),
            ],
            options={
                'verbose_name_plural': 'modules',
                'ordering': ('-created',),
                'verbose_name': 'module',
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('session', models.CharField(max_length=1000, verbose_name='session key')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('age', models.PositiveSmallIntegerField(verbose_name='age')),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=50, verbose_name='gender')),
                ('allow_info_usage', models.BooleanField(verbose_name='permission for publishing')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name_plural': 'participants',
                'ordering': ('-created',),
                'verbose_name': 'participant',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('processor', models.CharField(max_length=255, verbose_name='processor')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('image', sorl.thumbnail.fields.ImageField(blank=True, upload_to='survey/images', verbose_name='image')),
                ('short_description', models.TextField(blank=True, verbose_name='short description')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cognitive_tests.Module', verbose_name='module')),
            ],
            options={
                'verbose_name_plural': 'surveys',
                'abstract': False,
                'verbose_name': 'survey',
            },
        ),
        migrations.CreateModel(
            name='SurveyMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('key', models.SlugField(max_length=255, verbose_name='key')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('data_type', models.CharField(choices=[('NUMERIC', 'numeric'), ('STRING', 'string'), ('DATETIME', 'datetime'), ('NUMERIC_ARRAY', 'numeric array'), ('JSON', 'json')], default='NUMERIC', max_length=50, verbose_name='data types')),
                ('format', models.CharField(blank=True, max_length=255, verbose_name='format')),
                ('unit', models.CharField(blank=True, max_length=255, verbose_name='unit')),
                ('min_value', models.IntegerField(blank=True, null=True, verbose_name='min value')),
                ('max_value', models.IntegerField(blank=True, null=True, verbose_name='max value')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('visible', models.BooleanField(default=True, verbose_name='visible')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='cognitive_tests.Survey', verbose_name='survey')),
            ],
            options={
                'verbose_name_plural': 'survey marks',
                'abstract': False,
                'verbose_name': 'survey mark',
            },
        ),
        migrations.CreateModel(
            name='SurveyResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('processing_ended', models.DateTimeField(blank=True, null=True, verbose_name='processing ended')),
                ('processing_started', models.DateTimeField(blank=True, null=True, verbose_name='processing started')),
                ('is_completed', models.BooleanField(default=False, verbose_name='is completed')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_results', to='cognitive_tests.Participant', verbose_name='participant')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='cognitive_tests.Survey', verbose_name='survey')),
            ],
            options={
                'verbose_name_plural': 'survey results',
                'ordering': ('-created',),
                'verbose_name': 'survey result',
            },
        ),
        migrations.CreateModel(
            name='SurveyResultValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', jsonfield.fields.JSONField(verbose_name='value')),
                ('comment', models.TextField(blank=True, verbose_name='comment')),
                ('mark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='cognitive_tests.SurveyMark', verbose_name='mark')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='cognitive_tests.SurveyResult', verbose_name='result')),
            ],
            options={
                'verbose_name_plural': 'survey result values',
                'verbose_name': 'survey result value',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('processor', models.CharField(max_length=255, verbose_name='processor')),
                ('key', models.SlugField(max_length=255, unique=True, verbose_name='key')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('image', sorl.thumbnail.fields.ImageField(blank=True, upload_to='test/images', verbose_name='image')),
                ('short_description', models.TextField(blank=True, verbose_name='short description')),
                ('description', models.TextField(verbose_name='description')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('auto_save_data_to_file', models.BooleanField(default=False, verbose_name='auto save data to file')),
                ('web_index', models.CharField(blank=True, max_length=255, null=True, verbose_name='web index')),
                ('web_directory', models.CharField(blank=True, max_length=255, null=True, verbose_name='web folder')),
                ('web_record_audio', models.BooleanField(default=False, verbose_name='record audio')),
                ('web_record_video', models.BooleanField(default=False, verbose_name='record video')),
                ('web_record_mouse', models.BooleanField(default=False, verbose_name='record mouse')),
                ('web_instructions', models.TextField(blank=True, verbose_name='web instructions')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cognitive_tests.Module', verbose_name='module')),
            ],
            options={
                'verbose_name_plural': 'tests',
                'abstract': False,
                'verbose_name': 'test',
            },
        ),
        migrations.CreateModel(
            name='TestMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('key', models.SlugField(max_length=255, verbose_name='key')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('data_type', models.CharField(choices=[('NUMERIC', 'numeric'), ('STRING', 'string'), ('DATETIME', 'datetime'), ('NUMERIC_ARRAY', 'numeric array'), ('JSON', 'json')], default='NUMERIC', max_length=50, verbose_name='data types')),
                ('format', models.CharField(blank=True, max_length=255, verbose_name='format')),
                ('unit', models.CharField(blank=True, max_length=255, verbose_name='unit')),
                ('min_value', models.IntegerField(blank=True, null=True, verbose_name='min value')),
                ('max_value', models.IntegerField(blank=True, null=True, verbose_name='max value')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('visible', models.BooleanField(default=True, verbose_name='visible')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='cognitive_tests.Test', verbose_name='test')),
            ],
            options={
                'verbose_name_plural': 'test marks',
                'abstract': False,
                'verbose_name': 'test mark',
            },
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('processing_ended', models.DateTimeField(blank=True, null=True, verbose_name='processing ended')),
                ('processing_started', models.DateTimeField(blank=True, null=True, verbose_name='processing started')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_results', to='cognitive_tests.Participant', verbose_name='participant')),
                ('survey_result', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='test_results', to='cognitive_tests.SurveyResult', verbose_name='survey result')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='cognitive_tests.Test', verbose_name='test')),
            ],
            options={
                'verbose_name_plural': 'test results',
                'ordering': ('-created',),
                'verbose_name': 'test result',
            },
        ),
        migrations.CreateModel(
            name='TestResultFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='file name')),
                ('file', models.FileField(upload_to=cognitive_tests.models.TestResultFile.get_filename, verbose_name='file')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='cognitive_tests.TestResult', verbose_name='result')),
            ],
            options={
                'verbose_name_plural': 'result files',
                'verbose_name': 'result file',
            },
        ),
        migrations.CreateModel(
            name='TestResultTextData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='data name')),
                ('data', models.TextField(verbose_name='data')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_data', to='cognitive_tests.TestResult', verbose_name='result')),
            ],
            options={
                'verbose_name_plural': 'result text data',
                'verbose_name': 'result text data',
            },
        ),
        migrations.CreateModel(
            name='TestResultValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', jsonfield.fields.JSONField(verbose_name='value')),
                ('comment', models.TextField(blank=True, verbose_name='comment')),
                ('mark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='cognitive_tests.TestMark', verbose_name='mark')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='cognitive_tests.TestResult', verbose_name='result')),
            ],
            options={
                'verbose_name_plural': 'test result values',
                'verbose_name': 'test result value',
            },
        ),
        migrations.AddField(
            model_name='survey',
            name='tests',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='surveys', to='cognitive_tests.Test'),
        ),
        migrations.AlterUniqueTogether(
            name='testresultvalue',
            unique_together=set([('result', 'mark')]),
        ),
        migrations.AlterUniqueTogether(
            name='testresulttextdata',
            unique_together=set([('name', 'result')]),
        ),
        migrations.AlterUniqueTogether(
            name='testresultfile',
            unique_together=set([('name', 'result')]),
        ),
        migrations.AlterUniqueTogether(
            name='testresult',
            unique_together=set([('test', 'participant', 'survey_result')]),
        ),
        migrations.AlterUniqueTogether(
            name='testmark',
            unique_together=set([('test', 'key')]),
        ),
        migrations.AlterUniqueTogether(
            name='surveyresultvalue',
            unique_together=set([('result', 'mark')]),
        ),
        migrations.AlterUniqueTogether(
            name='surveymark',
            unique_together=set([('survey', 'key')]),
        ),
    ]
