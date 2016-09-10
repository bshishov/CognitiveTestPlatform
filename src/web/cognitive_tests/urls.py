from django.conf.urls import url, include
from rest_framework import routers
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from . import api_viewsets, api_views
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^participants/new$', views.participant_new, name='participant_new'),

    url(r'^web/check$', views.web_check, name='web_check'),

    url(r'^web/$', RedirectView.as_view(url=reverse_lazy('web_groups_list'))),
    url(r'^web/surveys$', views.web_group_list, name='web_groups_list'),
    url(r'^web/surveys/(?P<group_pk>[0-9]+)$', views.web_group_start, name='web_group'),
    url(r'^web/surveys/(?P<group_pk>[0-9]+)/start$', views.web_group_start, name='web_group_start'),
    url(r'^web/surveys/(?P<group_pk>[0-9]+)/(?P<order>[0-9]+)$', views.web_group_test, name='web_group_test'),
    url(r'^web/surveys/(?P<group_pk>[0-9]+)/results$', views.web_group_results, name='web_group_results'),


    url(r'^web/tests/$', views.web_test_list, name='web_tests_list'),
    url(r'^web/tests/(?P<test_pk>[0-9]+)$', views.web_test, name='web_tests'),


    url(r'^api/$', api_views.api_root),
    url(r'^api/participant/$', api_views.session_participant, name='session-participant'),
    url(r'^api/tests/$', api_views.test_list, name='test-list'),
    url(r'^api/tests/(?P<pk>[0-9]+)/$', api_views.test_detail, name='test-detail'),
    url(r'^api/tests/(?P<test_pk>[0-9]+)/results/$', api_views.test_results, name='test-results'),

    url(r'^api/', include('rest_framework.urls', namespace='rest_framework'))
]
