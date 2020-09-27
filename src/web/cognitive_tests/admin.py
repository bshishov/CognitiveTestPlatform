import logging
import os
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django import forms
from django.contrib import admin
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _

from django_ace import AceWidget
from pagedown.widgets import AdminPagedownWidget

from . import models
from . import utils


logger = logging.getLogger(__name__)

admin.site.site_header = _('Cognitive test platform')


def start_processing(model_admin, request, queryset):
    for item in queryset:
        if hasattr(item, 'process'):
            item.process()


start_processing.short_description = _('Start processing')


class IsProcessedListFilter(admin.SimpleListFilter):
    parameter_name = 'is_processed'
    title = _('Is processed')

    def lookups(self, request, model_admin):
        return (
            (True, _('True')),
            (False, _('False')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() in {True, 'True', 'true'}:
            return queryset.filter(processing_ended__isnull=False)

        if self.value() in {False, 'False', 'false'}:
            return queryset.filter(processing_ended__isnull=True)


@admin.register(models.Module)
class ModuleAdmin(admin.ModelAdmin):
    class ModuleForm(forms.ModelForm):
        UPLOAD_DIR = 'module_archives'
        full_path = forms.CharField(disabled=True, required=False, label=_('Full path'))
        archive = forms.FileField()

        def __init__(self, *args, **kwargs):
            super(ModuleAdmin.ModuleForm, self).__init__(*args, **kwargs)
            self.initial['full_path'] = self.instance.path

        def clean(self):
            data = super(ModuleAdmin.ModuleForm, self).clean()
            archive = data.get('archive', None)
            logger.info('Saving module archive: %s' % archive)
            upload_dir = os.path.join(settings.MEDIA_ROOT, self.UPLOAD_DIR)
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            target_location = os.path.join(upload_dir, archive.name)
            utils.save_file_to(self['archive'].value(), target_location)
            try:
                models.Module.objects.import_from_zip(target_location, module=self.instance, commit=False)
            except Exception as err:
                print(err)
                raise ValidationError(_('Failed to load archive, expected .zip'), code='invalid')
            finally:
                os.remove(target_location)

        def save_m2m(self):
            self._save_m2m()

        class Meta:
            model = models.Module
            fields = ('archive',)

    form = ModuleForm


@admin.register(models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'age', 'gender', 'allow_info_usage', 'email', 'created')
    list_filter = ('user', 'age', 'gender', 'allow_info_usage', 'email')
    search_fields = ['name']


@admin.register(models.Test)
class TestAdmin(admin.ModelAdmin):
    class MarksInlineForm(admin.StackedInline):
        model = models.TestMark
        extra = 0

    list_display = ('name', 'active', 'created')
    list_filter = ('active', 'created')
    search_fields = ['name', 'description']
    inlines = [MarksInlineForm, ]
    formfield_overrides = {models.models.TextField: {'widget': AdminPagedownWidget()}, }


@admin.register(models.TestMark)
class TestMarkAdmin(admin.ModelAdmin):
    list_display = ('name', 'test', 'key', 'data_type', 'format', 'unit', 'visible', 'created')
    list_filter = ('test', 'data_type', 'format', 'visible', 'created')
    search_fields = ['name', 'description', 'test__name']
    formfield_overrides = {models.models.TextField: {'widget': AdminPagedownWidget()}, }


@admin.register(models.TestResult)
class TestResultAdmin(admin.ModelAdmin):
    class FilesInlineForm(admin.TabularInline):
        model = models.TestResultFile
        extra = 0

    class TextDataInlineForm(admin.TabularInline):
        model = models.TestResultTextData
        extra = 0

    class ValuesInlineForm(admin.TabularInline):
        model = models.TestResultValue
        extra = 0

    list_display = ('participant', 'test', 'created', 'is_processed')
    list_filter = (IsProcessedListFilter, 'test', 'created', 'participant')
    search_fields = ['test__name', 'participant__name', ]
    inlines = [FilesInlineForm, TextDataInlineForm, ValuesInlineForm]
    actions = [start_processing, ]

    def is_processed(self, obj):
        return obj.is_processed


@admin.register(models.TestResultFile)
class TestResultFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'result', 'file',)
    list_filter = ('name', 'result__test', 'result__created')
    search_fields = ['name', 'result__participant__name', ]


@admin.register(models.TestResultTextData)
class TestResultTextDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'result', )
    list_filter = ('name', 'result__test', 'result__created')
    search_fields = ['name', 'result__participant__name', ]


@admin.register(models.TestResultValue)
class TestResultValueAdmin(admin.ModelAdmin):
    list_display = ('result', 'mark', 'value',)
    list_filter = ('mark', 'result__created')
    search_fields = ['mark', 'result__participant__name', ]


@admin.register(models.Survey)
class SurveyAdmin(admin.ModelAdmin):
    class MarksInlineForm(admin.StackedInline):
        model = models.SurveyMark
        extra = 0

    list_display = ('name', 'active', 'created')
    list_filter = ('active', 'created')
    search_fields = ['name', 'description']
    inlines = [MarksInlineForm, ]
    formfield_overrides = {models.models.TextField: {'widget': AdminPagedownWidget()}, }


@admin.register(models.SurveyMark)
class SurveyMarkAdmin(admin.ModelAdmin):
    list_display = ('name', 'survey', 'key', 'data_type', 'format', 'unit', 'visible', 'created')
    list_filter = ('survey', 'data_type', 'format', 'visible', 'created')
    search_fields = ['name', 'description', 'survey__name']
    formfield_overrides = {models.models.TextField: {'widget': AdminPagedownWidget()}, }


@admin.register(models.SurveyResult)
class SurveyResultAdmin(admin.ModelAdmin):
    class ValuesInlineForm(admin.TabularInline):
        model = models.SurveyResultValue
        extra = 0

    list_display = ('participant', 'survey', 'is_completed', 'created', 'is_processed')
    list_filter = (IsProcessedListFilter, 'survey', 'is_completed', 'created', 'participant')
    search_fields = ['survey__name', 'participant__name', ]
    inlines = [ValuesInlineForm, ]
    actions = [start_processing, ]

    def is_processed(self, obj):
        return obj.is_processed


@admin.register(models.SurveyResultValue)
class SurveyResultValueAdmin(admin.ModelAdmin):
    list_display = ('result', 'mark', 'value',)
    list_filter = ('mark', 'result__created')
    search_fields = ['mark', 'result__participant__name', ]
