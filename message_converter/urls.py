#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
# from django.conf.urls.defaults import *
from message_converter.views import FlatFileView

urlpatterns = patterns('',
                       # this URL passes resource_id in **kw to MyRESTView
                       # url(r'^api/v1.0/resource/(?P<resource_id>\d+)[/]?$', FlatFileView.as_view(), name='create_flat_file_view'),
                       url(r'^api/v1.0/flat-file[/]?$', FlatFileView.as_view(), name='create_flat_file_view'),)

