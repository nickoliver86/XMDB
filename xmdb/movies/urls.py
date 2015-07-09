from django.conf.urls import url, patterns, include

from . import views

urlpatterns = patterns('movies.views',
    url(r'^$', 'IndexTest'),
)
