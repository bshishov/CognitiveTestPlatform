from django.conf.urls import url, include
from rest_framework import routers
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

from . import views
from . import api_viewsets


urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^participants/new$', views.participant_new, name='participant_new'),

    url(r'^surveys/$', views.surveys, name='surveys'),
    url(r'^surveys/(?P<survey_pk>[0-9]+)$', views.survey_view, name='survey'),
    url(r'^surveys/(?P<survey_pk>[0-9]+)/start$', views.survey_start, name='survey-start'),
    url(r'^surveys/(?P<survey_pk>[0-9]+)/check', views.survey_check, name='survey-check'),
    url(r'^surveys/run/(?P<survey_result_pk>[0-9]+)/continue', views.survey_continue, name='survey-continue'),
    url(r'^surveys/run/(?P<survey_result_pk>[0-9]+)/tests/(?P<test_pk>[0-9]+)$', views.survey_test, name='survey-test'),
    url(r'^surveys/run/(?P<survey_result_pk>[0-9]+)/end', views.survey_end, name='survey-end'),
    url(r'^surveys/run/(?P<survey_result_pk>[0-9]+)/results$', views.survey_results, name='survey-results'),

    url(r'^tests/(?P<test_pk>[0-9]+)/$', views.test_view, name='test'),
    url(r'^tests/(?P<test_pk>[0-9]+)/start', views.test_start, name='test-start'),
    url(r'^tests/(?P<test_pk>[0-9]+)/check$', views.test_check, name='test-check'),
    url(r'^tests/(?P<test_pk>[0-9]+)/run', views.test_run, name='test-run'),
    url(r'^tests/(?P<test_pk>[0-9]+)/results', views.test_results, name='test-results'),
    url(r'^tests/(?P<test_pk>[0-9]+)/embed/(?P<path>[^?]*)$', views.test_embed, name='test-embed'),
]


api_router = routers.DefaultRouter()
api_router.register(r'modules', api_viewsets.ModuleViewSet, base_name='module')
api_router.register(r'participants', api_viewsets.ParticipantViewSet, base_name='participant')
api_router.register(r'tests', api_viewsets.TestViewSet, base_name='test')
api_router.register(r'testmarks', api_viewsets.TestMarkViewSet, base_name='testmark')
api_router.register(r'testresults', api_viewsets.TestResultViewSet, base_name='testresult')
api_router.register(r'testresulttextdata', api_viewsets.TestResultTextDataViewSet, base_name='testresulttextdata')
api_router.register(r'testresultfiles', api_viewsets.TestResultFileViewSet, base_name='testresultfile')
api_router.register(r'surveys', api_viewsets.SurveyViewSet, base_name='survey')
api_router.register(r'surveymarks', api_viewsets.SurveyMarkViewSet, base_name='surveymark')
api_router.register(r'surveyresults', api_viewsets.SurveyResultViewSet, base_name='surveyresult')


urlpatterns += [
    url(r'^api/', include(api_router.urls, namespace='api')),
]
