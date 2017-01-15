from django.conf.urls import url, include
from rest_framework import routers
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from . import api_views
from . import views


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

    url(r'^api/$', api_views.api_root),
    url(r'^api/participant/$', api_views.session_participant, name='session-participant'),

    url(r'^api/tests/$', api_views.test_list, name='test-list'),
    url(r'^api/tests/(?P<pk>[0-9]+)/$', api_views.test_detail, name='test-detail'),
    url(r'^api/tests/(?P<pk>[0-9]+)/results/$', api_views.test_results, name='test-results'),
    url(r'^api/tests/(?P<pk>[0-9]+)/marks/$', api_views.test_marks, name='test-marks'),

    url(r'^api/testresulttextdata/(?P<pk>[0-9]+)/$', api_views.test_result_text_data_detail, name='testresulttextdata-detail'),
    url(r'^api/testresultfile/(?P<pk>[0-9]+)/$', api_views.test_result_file_detail, name='testresultfile-detail'),

    url(r'^api/', include('rest_framework.urls', namespace='rest_framework'))
]
