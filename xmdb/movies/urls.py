from django.conf.urls import url, patterns, include

from . import views

urlpatterns = [
    url(r'^$', views.IndexTest, name='IndexTest'),
    url(r'signup/$', views.UserSignUp, name ='UserSignUp'),
    url(r'signin/$', views.signin, name ='signin'),
    url(r'movie_list/$', views.MovieList, name='MovieList'),
    url(r'^movie_summary/(\d+)/$', views.MovieSummary, name='MovieSummary'),
    url(r'search/$', views.Search, name ='Search'),
    url(r'^add_to_library/(\w+)/$', views.AddToLibrary, name='add_to_library'),
]
