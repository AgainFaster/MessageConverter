from django.conf.urls import patterns, include, url

from django.contrib import admin
from message_converter import urls as message_converter_urls

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MessageConverter.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^message_converter/', include(message_converter_urls)),
)
