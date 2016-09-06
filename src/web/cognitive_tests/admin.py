from django.contrib import admin
from .models import *

admin.site.register(Participant)
admin.site.register(Test)
admin.site.register(WebTest)
admin.site.register(TestResult)
