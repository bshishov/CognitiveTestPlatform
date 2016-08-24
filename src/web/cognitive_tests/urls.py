from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^start$', views.start, name='start'),
    url(r'^list', views.list, name='list'),
    url(r'^first', views.first, name='first'),
    url(r'^check', views.check, name='check'),
    url(r'^result', views.result, name='result'),
    url(r'^test/(?P<test_name>.+)', views.test, name='test'),
]
