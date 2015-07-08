from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^movies/', include('movies.urls', namespace="movies")),
    url(r'^admin/', include(admin.site.urls)),
]