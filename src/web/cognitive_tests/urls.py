from django.conf.urls import url, include
from rest_framework import routers
from . import api_viewsets, api_views
from . import views

#api_router = routers.DefaultRouter()
#api_router.register(r'^participants', api_viewsets.ParticipantViewSet, 'Participant')
#api_router.register(r'^test_results', api_viewsets.TestViewSet, 'TestResult')
#api_router.register(r'^tests', api_viewsets.TestViewSet, 'Test')
#api_router.register(r'^web_tests', api_viewsets.WebTestViewSet, 'WebTest')

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^start$', views.start, name='start'),
    url(r'^list', views.list, name='list'),
    url(r'^first', views.first, name='first'),
    url(r'^check', views.check, name='check'),
    url(r'^result', views.result, name='result'),
    url(r'^test/(?P<test_id>.+)', views.web_test, name='test'),
    #url(r'^api/', include(api_router.urls)),

    url(r'^api/$', api_views.api_root),
    url(r'^api/tests/$', api_views.test_list, name='test-list'),
    url(r'^api/tests/(?P<pk>[0-9]+)/$', api_views.test_detail, name='test-detail'),
    url(r'^api/tests/(?P<test_pk>[0-9]+)/results/$', api_views.test_results, name='test-results'),

    url(r'^api/', include('rest_framework.urls', namespace='rest_framework'))
]
