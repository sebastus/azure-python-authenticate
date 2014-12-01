from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'aadrest.views.index', name='index'),
	url(r'^step1/$', 'aadrest.views.step1', name='step1'),
	url(r'^step2/$', 'aadrest.views.step2', name='step2'),
	url(r'^step3/$', 'aadrest.views.step3', name='step3'),
	url(r'^step4/$', 'aadrest.views.step4', name='step4'),
	url(r'^step1_live/$', 'aadrest.views.step1_live', name='step1_live'),
	url(r'^step2_live/$', 'aadrest.views.step2_live', name='step2_live'),
	url(r'^step3_live/$', 'aadrest.views.step3_live', name='step3_live'),
	url(r'^step4_live/$', 'aadrest.views.step4_live', name='step4_live'),
)