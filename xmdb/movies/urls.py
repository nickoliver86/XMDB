from django.conf.urls import url, patterns, include

from . import views

urlpatterns = [
    url(r'^$', views.IndexTest, name='IndexTest'),
    url(r'signup/$', views.UserSignUp, name ='UserSignUp'),
    url(r'movie_list/$', views.MovieList, name='MovieList'),
    url(r'^movie_summary/(\d+)/$', views.MovieSummary, name='MovieSummary'),
]
