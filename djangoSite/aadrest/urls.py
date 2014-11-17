from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'aadrest.views.index', name='index'),
	url(r'^step2/$', 'aadrest.views.step2', name='step2'),
	url(r'^step3/$', 'aadrest.views.step3', name='step3'),
	url(r'^step4/$', 'aadrest.views.step4', name='step4'),
)