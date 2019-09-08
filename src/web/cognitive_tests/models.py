# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import shutil
import logging
import zipfile

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver, Signal

from jsonfield import JSONField
from sortedm2m.fields import SortedManyToManyField
from sorl.thumbnail import ImageField

from .tasks import run_async
from .run_tools import run

logger = logging.getLogger(__name__)


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-managed "created" and
    "modified" fields, borrowed from django_extensions.
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))

    class Meta:
        ordering = ('-created',)
        abstract = True


class ModuleManager(models.Manager):
    @staticmethod
    def import_from_zip(path_to_zip, module=None, commit=False):
        logger.info('Importing module from archive')
        name = os.path.basename(os.path.splitext(path_to_zip)[0])
        module_path = os.path.join(settings.TESTS_MODULES_DIR, name)

        if module:
            if module.path and os.path.exists(module.path):
                shutil.rmtree(module.path)

        with zipfile.ZipFile(path_to_zip, 'r') as zip_file:
            zip_file.extractall(module_path)
        if module:
            module.path = module_path
            info_path = os.path.join(module_path, Module.INFO_FILE)
            if os.path.exists(info_path):
                with open(info_path, 'r') as info_file:
                    module.info = info_file.read()
            else:
                module.info = ''
        else:
            module = Module.objects.create(path=module_path, info='')
        if commit:
            module.save()
        return module

    @staticmethod
    def import_from_git(self, git_url):
        logger.info('Importing module from git')
        raise NotImplementedError('Import from git is not implemented')


class Module(TimeStampedModel):
    INFO_FILE = 'module.json'
    objects = ModuleManager()

    info = JSONField(verbose_name=_('information'))
    path: str = models.FilePathField(path=settings.TESTS_MODULES_DIR, allow_files=False,
                                     allow_folders=True, recursive=False, verbose_name=_('path'))

    class Meta:
        ordering = ('-created',)
        verbose_name = _('module')
        verbose_name_plural = _('modules')

    def __str__(self):  # __unicode__ on Python 2
        return '%s' % (os.path.basename(self.path),)


@receiver(post_delete, sender=Module, dispatch_uid="module_post_delete")
def __post_module_delete(sender, instance, **kwargs):
    if os.path.isdir(instance.path):
        logger.debug('Removing module directory: %s' % instance.path)
        shutil.rmtree(instance.path)


class ModuleProcessor(models.Model):
    """ Base class for models that can process results, e.g. Test and Survey """
    module: 'Module' = models.ForeignKey(Module, blank=False, null=False, verbose_name=_('module'))
    processor: str = models.CharField(max_length=255, blank=False, null=False, verbose_name=_('processor'))

    class Meta:
        abstract = True

    def clean_fields(self, exclude=None):
        if not os.path.exists(self.get_processor_path()):
            return ValidationError({'processor': _('Processor file does not exist')})

    def get_processor_path(self):
        if self.processor is None:
            return None
        return os.path.join(self.module.path, self.processor)

    @run_async
    def process(self, instance: 'ProcessableModel', arguments: dict = None, run_name='main'):
        logger.info('Processing of %s by %s' % (repr(instance), repr(self)))

        marks = list(self.marks.all())
        logger.debug('Marks: %s' % repr(marks))

        if not isinstance(instance, ProcessableModel):
            raise TypeError('ProcessableModel expected')

        try:
            instance.begin_process(self)
            process_globals = run(self.processor, inputs=arguments, work_dir=self.module.path)
            for mark in marks:
                if mark.key not in process_globals:
                    raise LookupError('Key %s was nit found in result globals' % mark.key)
                mark.values.create(result=instance, value=process_globals[mark.key],
                                   comment=process_globals.get(mark.key + '_comment', ''))
            instance.end_process(self)
        except Exception as err:
            logger.exception(err)
            instance.processing_failed(self)


class ProcessableModel(models.Model):
    processing_ended = models.DateTimeField(blank=True, null=True, verbose_name=_('processing ended'))
    processing_started = models.DateTimeField(blank=True, null=True, verbose_name=_('processing started'))

    class Meta:
        abstract = True

    def begin_process(self, processor):
        if self.is_processed:
            raise RuntimeError('Can\'t begin processing: instance is already processed')

        if self.is_processing_started:
            raise RuntimeError('Can\'t begin processing: processing of this instance is already started')

        self.processing_started = timezone.now()
        self.save()

    def process(self):
        raise NotImplementedError('This method is abstract')

    def end_process(self, processor):
        self.processing_ended = timezone.now()
        self.save()

    def processing_failed(self, processor):
        self.processing_started = None
        self.processing_ended = None
        self.save()

    @property
    def is_processed(self):
        return self.processing_ended is not None

    @property
    def is_processing_started(self):
        return self.processing_started is not None


class MarkManager(models.Manager):
    def visible(self):
        return self.get_queryset().filter(visible=True)


class Mark(models.Model):
    NUMERIC = 'NUMERIC'
    STRING = 'STRING'
    DATETIME = 'DATETIME'
    NUMERIC_ARRAY = 'NUMERIC_ARRAY'
    JSON = 'JSON'

    DATA_TYPES = (
        (NUMERIC, _('numeric')),
        (STRING, _('string')),
        (DATETIME, _('datetime')),
        (NUMERIC_ARRAY, _('numeric array')),
        (JSON, _('json')),
    )

    CMP_NO = 'NO'
    CMP_HIGHER_IS_BETTER = 'HIGHER_IS_BETTER'
    CMP_LOWER_IS_BETTER = 'LOWER_IS_BETTER'

    NUMERIC_COMPARE = (
        (CMP_NO, 'No comparison'),
        (CMP_HIGHER_IS_BETTER, 'Higher is better'),
        (CMP_LOWER_IS_BETTER, 'Lower is better'),
    )

    objects = MarkManager()

    key = models.SlugField(max_length=255, verbose_name=_('key'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    data_type = models.CharField(max_length=50, choices=DATA_TYPES, verbose_name=_('data types'), default=NUMERIC)
    cmp = models.CharField(max_length=50, choices=NUMERIC_COMPARE, verbose_name='Numeric comparison', default=CMP_NO)
    format = models.CharField(max_length=255, verbose_name=_('format'), blank=True)
    unit = models.CharField(max_length=255, verbose_name=_('unit'), blank=True)
    min_value = models.IntegerField(blank=True, null=True, verbose_name=_('min value'))
    max_value = models.IntegerField(blank=True, null=True, verbose_name=_('max value'))
    description = models.TextField(verbose_name=_('description'), blank=True)
    visible = models.BooleanField(verbose_name=_('visible'), default=True)

    class Meta:
        abstract = True


class Participant(TimeStampedModel):
    PARTICIPANT_SESSION_KEY = 'participant_id'
    MALE = 'male'
    FEMALE = 'female'
    GENDER_CHOICES = (
        (MALE, _('male')),
        (FEMALE, _('female'))
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name=_('user'))
    session = models.CharField(max_length=1000, verbose_name=_('session key'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    age = models.PositiveSmallIntegerField(verbose_name=_('age'))
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, verbose_name=_('gender'))
    allow_info_usage = models.BooleanField(verbose_name=_('permission for publishing'))
    email = models.EmailField(blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('participant')
        verbose_name_plural = _('participants')

    def __str__(self):  # __unicode__ on Python 2
        return '%s %s' % (self.name, self.age)

    @classmethod
    def from_request(cls, request):
        if Participant.PARTICIPANT_SESSION_KEY not in request.session:
            return None
        try:
            return Participant.objects.filter(session=request.session.session_key).first()
        except:
            del request.session[Participant.PARTICIPANT_SESSION_KEY]
            return None

    def assign_to_request(self, request):
        request.session[Participant.PARTICIPANT_SESSION_KEY] = self.session

    def unassign_from_request(self, request):
        del request.session[Participant.PARTICIPANT_SESSION_KEY]


class TestManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(active=True)

    def active_web(self):
        """ Filter only active tests with web directory set """
        return self.get_queryset().filter(active=True) \
            .exclude(web_directory__isnull=True).exclude(web_directory__exact='')


class Test(TimeStampedModel, ModuleProcessor):
    objects = TestManager()

    key = models.SlugField(max_length=255, unique=True, verbose_name=_('key'))
    name = models.CharField(max_length=255, verbose_name=_('name'))
    image = ImageField(upload_to='test/images', blank=True, verbose_name=_('image'))
    short_description = models.TextField(verbose_name=_('short description'), blank=True)
    description = models.TextField(verbose_name=_('description'))
    active = models.BooleanField(default=True, verbose_name=_('active'))
    auto_save_data_to_file = models.BooleanField(default=False, verbose_name=_('auto save data to file'))
    web_index = models.CharField(max_length=255, verbose_name=_('web index'), blank=True, null=True)
    web_directory = models.CharField(max_length=255, verbose_name=_('web folder'), blank=True, null=True)
    web_record_audio = models.BooleanField(default=False, verbose_name=_('record audio'))
    web_record_video = models.BooleanField(default=False, verbose_name=_('record video'))
    web_record_mouse = models.BooleanField(default=False, verbose_name=_('record mouse'))
    web_instructions = models.TextField(verbose_name=_('web instructions'), blank=True)

    class Meta(ModuleProcessor.Meta):
        verbose_name = _('test')
        verbose_name_plural = _('tests')

    def __str__(self):  # __unicode__ on Python 2
        return '%s' % self.name

    @property
    def web_is_active(self):
        if self.web_directory is None:
            return False
        if self.web_directory is '':
            return False
        return True

    def get_web_directory_path(self):
        if self.web_directory is None:
            return None
        return os.path.join(self.module.path, self.web_directory)

    def get_web_index_path(self):
        if self.web_index is None:
            return None
        return os.path.join(self.get_web_directory_path(), self.web_index)

    def clean_fields(self, exclude=None):
        ModuleProcessor.clean_fields(self, exclude=exclude)
        if self.web_is_active:
            if not os.path.isdir(self.get_web_directory_path()):
                return ValidationError({'web_directory', _('Incorrect web directory path')})

            if not os.path.exists(self.get_web_index_path()):
                return ValidationError({'web_index', _('Web index file does not exist')})

    def get_result_for(self, participant):
        try:
            return self.results.filter(participant=participant)[:1].get()
        except ObjectDoesNotExist:
            return None

    def get_all_results_for(self, participant):
        return self.results.filter(participant=participant)


class TestMark(TimeStampedModel, Mark):
    test = models.ForeignKey(Test, related_name='marks', verbose_name=_('test'))

    class Meta(Mark.Meta):
        verbose_name = _('test mark')
        verbose_name_plural = _('test marks')
        unique_together = ('test', 'key')

    def __str__(self):  # __unicode__ on Python 2
        return '%s (%s)' % (self.name, self.test)


class TestResult(TimeStampedModel, ProcessableModel):
    participant = models.ForeignKey(Participant, related_name='test_results', verbose_name=_('participant'))
    test = models.ForeignKey(Test, related_name='results', verbose_name=_('test'))
    survey_result = models.ForeignKey('SurveyResult', blank=True, null=True, on_delete=models.DO_NOTHING,
                                      related_name='test_results', verbose_name=_('survey result'))

    def __str__(self):  # __unicode__ on Python 2
        return "%s (%s)" % (self.test, self.participant)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('test result')
        verbose_name_plural = _('test results')
        # test-survey_result constraint: should be only one test result for a specific test per survey result
        unique_together = ('test', 'participant', 'survey_result')

    def process(self):
        self.test.process(self, {
            'files': dict((file.name, file.file.storage.path(file.file.name)) for file in self.files.all()),
            'text_data': dict((data.name, data.data) for data in self.text_data.all()),
        }, run_name=self.test.key)


@receiver(pre_save, sender=TestResult)
def __test_result_pre_save(sender, instance, **kwargs):
    # if there is a new result for a survey then unbind previous result from a survey
    # constraint is still valid and user can retry tests
    if instance.survey_result is not None:
        try:
            last = TestResult.objects.get(survey_result=instance.survey_result, test=instance.test)
            last.survey_result = None
            logger.debug('Removed test-result %s from survey-result %s' % (last, instance.survey_result))
            last.save()
        except ObjectDoesNotExist:
            pass


class TestResultFile(models.Model):
    def get_filename(self, filename):
        return 'results/%s_test%s_p%s/raw/%s' % (
        self.result.id, self.result.test.id, self.result.participant.id, filename)

    name = models.CharField(max_length=255, verbose_name=_('file name'))
    result = models.ForeignKey(TestResult, related_name='files', verbose_name=_('result'))
    file = models.FileField(upload_to=get_filename, verbose_name=_('file'))

    class Meta:
        verbose_name = _('result file')
        verbose_name_plural = _('result files')
        unique_together = ('name', 'result')

    def __str__(self):  # __unicode__ on Python 2
        return '%s (%s)' % (self.name, self.result)


@receiver(post_delete, sender=TestResultFile)
def __test_result_file_post_delete(sender, instance, **kwargs):
    logger.debug('Deleting file (%s)' % instance)
    instance.file.delete(save=False)


class TestResultTextData(models.Model):
    RESTRICTED_NAMES = ('id', 'csrfmiddlewaretoken', 'survey_result')

    name = models.CharField(max_length=255, verbose_name=_('data name'))
    result = models.ForeignKey(TestResult, related_name='text_data', verbose_name=_('result'))
    data = models.TextField(verbose_name=_('data'))

    def __str__(self):  # __unicode__ on Python 2
        return '%s (%s)' % (self.name, self.result)

    class Meta:
        verbose_name = _('result text data')
        verbose_name_plural = _('result text data')
        unique_together = ('name', 'result')


@receiver(post_save, sender=TestResultTextData, dispatch_uid="post_text_data_save")
def __post_text_data_save(sender, instance, **kwargs):
    """
    :type instance: TestResultTextData
    """
    logger.debug('Post text data save')
    if instance.result.test.auto_save_data_to_file:
        logger.debug('Saving text data to file')
        filename = '%s.txt' % instance.name
        try:
            test_result_file = TestResultFile.objects.get(name=instance.name, result=instance.result)
            logger.debug('Result file is already exists, overwriting')
            test_result_file.file.delete(save=False)
        except ObjectDoesNotExist:
            test_result_file = TestResultFile(name=instance.name, result=instance.result)
            logger.debug('Result file does not exist')
        test_result_file.file.save(filename, ContentFile(instance.data), save=False)
        test_result_file.save()


class TestResultValueManager(models.Manager):
    def visible(self):
        return self.get_queryset().filter(mark__visible=True)


class TestResultValue(models.Model):
    objects = TestResultValueManager()

    result = models.ForeignKey(TestResult, related_name='values', verbose_name=_('result'))
    mark = models.ForeignKey(TestMark, related_name='values', verbose_name=_('mark'))
    value = JSONField(verbose_name=_('value'))
    comment = models.TextField(verbose_name=_('comment'), blank=True)

    def __str__(self):  # __unicode__ on Python 2
        return '%s (%s)' % (self.value, self.mark)

    class Meta:
        verbose_name = _('test result value')
        verbose_name_plural = _('test result values')
        unique_together = ('result', 'mark')


class SurveyManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(active=True)


class Survey(TimeStampedModel, ModuleProcessor):
    objects = SurveyManager()

    active = models.BooleanField(default=True, verbose_name=_('active'))
    tests = SortedManyToManyField(Test, related_name='surveys')
    name = models.CharField(max_length=255, verbose_name=_('name'))
    image = ImageField(upload_to='survey/images', blank=True, verbose_name=_('image'))
    short_description = models.TextField(verbose_name=_('short description'), blank=True)
    description = models.TextField(verbose_name=_('description'), blank=True)

    class Meta(ModuleProcessor.Meta):
        verbose_name = _('survey')
        verbose_name_plural = _('surveys')

    def __str__(self):  # __unicode__ on Python 2
        return '%s' % (self.name,)

    def get_result_for(self, participant):
        try:
            return self.results.filter(participant=participant)[:1].get()
        except ObjectDoesNotExist:
            return None

    def get_all_results_for(self, participant):
        return self.results.filter(participant=participant)

    @property
    def web_record_audio(self):
        return len(self.tests.active_web().filter(web_record_audio=True)) > 0

    @property
    def web_record_video(self):
        return len(self.tests.active_web().filter(web_record_video=True)) > 0


class SurveyMark(TimeStampedModel, Mark):
    survey = models.ForeignKey(Survey, related_name='marks', verbose_name=_('survey'))

    class Meta(Mark.Meta):
        verbose_name = _('survey mark')
        verbose_name_plural = _('survey marks')
        unique_together = ('survey', 'key')

    def __str__(self):  # __unicode__ on Python 2
        return '%s (%s)' % (self.name, self.survey)


class SurveyResult(TimeStampedModel, ProcessableModel):
    survey = models.ForeignKey(Survey, related_name='results', verbose_name=_('survey'))  # type: Survey
    participant = models.ForeignKey(Participant, related_name='survey_results', verbose_name=_('participant'))
    is_completed = models.BooleanField(default=False, verbose_name=_('is completed'))

    class Meta:
        ordering = ('-created',)
        verbose_name = _('survey result')
        verbose_name_plural = _('survey results')

    def __str__(self):  # __unicode__ on Python 2
        return '%s (%s)' % (self.survey, self.participant)

    def process(self):
        if not self.is_completed:
            raise RuntimeError('Can not start processing, survey is not completed')
        arguments = {}
        for test in self.survey.tests.all():
            test_result = test.get_result_for(self.participant)
            if test_result is None:
                raise RuntimeError('No result for %s' % test_result)
            result_values = test_result.values.all()
            test_values_dict = {}
            for val in result_values:
                test_values_dict[val.mark.key] = val.value
            arguments[test.key] = test_values_dict
        self.survey.process(self, {'test_results': arguments})

    @property
    def incomplete_tests(self):
        # find all the tests of this survey result, then exclude every test which has a result
        return self.survey.tests.all().exclude(results__survey_result=self)


class SurveyResultValueManager(models.Manager):
    def visible(self):
        return self.get_queryset().filter(mark__visible=True)


class SurveyResultValue(models.Model):
    objects = SurveyResultValueManager()

    result = models.ForeignKey(SurveyResult, related_name='values', verbose_name=_('result'))
    mark = models.ForeignKey(SurveyMark, related_name='values', verbose_name=_('mark'))
    value = JSONField(verbose_name=_('value'))
    comment = models.TextField(verbose_name=_('comment'), blank=True)

    class Meta:
        verbose_name = _('survey result value')
        verbose_name_plural = _('survey result values')
        unique_together = ('result', 'mark')

    def __str__(self):  # __unicode__ on Python 2
        return '%s (%s)' % (self.value, self.mark)
