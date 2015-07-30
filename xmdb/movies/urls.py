from django.conf.urls import url, patterns, include

from movies import views

urlpatterns = [
    url(r'^$', views.index_test, name='IndexTest'),
    url(r'signup/$', views.user_sign_up, name ='UserSignUp'),
    url(r'signin/$', views.sign_in, name ='signin'),
    url(r'signout/$', views.sign_out, name ='signout'),
    url(r'movie_list/$', views.pagination, name='MovieList'),
    # url(r'movie_list/$', views.movie_list, name='MovieList'),
    url(r'^movie_summary/(\w+)/$', views.movie_summary, name='MovieSummary'),
    url(r'search/$', views.search, name ='Search'),
    url(r'^add_to_library/(\w+)/$', views.add_to_library, name='add_to_library'),
    url(r'^remove_from_library/(\w+)/$', views.remove_from_library, name='remove_from_library'),
]
