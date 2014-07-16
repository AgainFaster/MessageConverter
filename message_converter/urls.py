#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
# from django.conf.urls.defaults import *
from message_converter.views import ApiProjectView

urlpatterns = patterns('',
                       url(r'^api/(?P<project_name>[\w-]+)[/]?$', ApiProjectView.as_view(), name='api_project_view'),)

