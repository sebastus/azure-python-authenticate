from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'oauth.views.index', name='index'),
	url(r'^step1/$', 'oauth.views.step1', name='step1'),
	url(r'^step2/$', 'oauth.views.step2', name='step2'),
)