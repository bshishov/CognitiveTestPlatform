from django.contrib import admin
from django.forms import ModelForm
from .models import *
from django_ace import AceWidget
from pagedown.widgets import AdminPagedownWidget
from django.template.defaultfilters import truncatechars
from django.utils.translation import ugettext_lazy as _


admin.site.site_header = _('Cognitive test platform')

admin.site.register(Module)
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
