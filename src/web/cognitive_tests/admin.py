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

from .models import *
from .utils import *


logger = logging.getLogger(__name__)

admin.site.site_header = _('Cognitive test platform')


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
            save_file_to(self['archive'].value(), target_location)
            try:
                Module.objects.import_from_zip(target_location, module=self.instance, commit=False)
            except Exception as err:
                print(err)
                raise ValidationError(_('Failed to load archive, expected .zip'), code='invalid')
            finally:
                os.remove(target_location)

        def save_m2m(self):
            self._save_m2m()

        class Meta:
            model = Module
            fields = ('archive',)

    form = ModuleForm


admin.site.register(Module, ModuleAdmin)
admin.site.register(Participant)
admin.site.register(Survey)
admin.site.register(SurveyMark)
admin.site.register(SurveyResult)
admin.site.register(SurveyResultValue)
admin.site.register(Test)
admin.site.register(TestMark)
admin.site.register(TestResult)
admin.site.register(TestResultFile)
admin.site.register(TestResultTextData)
admin.site.register(TestResultValue)
