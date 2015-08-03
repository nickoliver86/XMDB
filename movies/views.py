from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views import generic
from django.contrib.auth.models import User
from movies.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import requests
from django import forms, views
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pdb
# Create your views here.

# FIXME Regarding naming conventions, best to follow pep-8. --fixed
# methods should be lower case and words separated by underscores
# Classes can be first letter capitalized (not camel case), no underscores

def index_test(request):
    return render(request, 'movies/index.html')

def sign_in(request):
    # FIXME What if user is already logged in?  -- fixed
    if request.method == 'POST':
        un = request.POST.get('username')
        pw = request.POST.get('password')
        user = authenticate(username=un, password=pw)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('movies:IndexTest'))
            else:
                return HttpResponseRedirect("Your account is disabled.")
        else:
            #print('Invalid login details: {0}, {1}'.format(un, pw))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'movies/signin.html', {})

def user_sign_up(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("")
        else:
            form = UserCreationForm()
    return render(request, "movies/index.html")

def movie_summary(request, movie_id, search_query=None):

    if not request.user.is_authenticated or request.user.is_anonymous:
        movielist = Movie.objects.all()
    else:
        movielist = request.user.movie_set.all()
    try:
        m = movielist.get(imdbId=movie_id)
    except Movie.DoesNotExist:
        r = requests.get('http://www.omdbapi.com/?i={0}&plot=short&r=json'.format(movie_id))
        imdb = r.json().get('imdbID')
        themoviedb = requests.get('http://api.themoviedb.org/3/movie/{0}?external_source=imdb_id/images&api_key=a922b176fe232a0599b7a991011c6dd6'.format(imdb))
        themoviedb.encoding = 'ISO-8859-1'
        poster_url = themoviedb.json().get('poster_path')[1:]
        d = Director.objects.get_or_create(name=r.json().get('Director'))[0]
        w = Writer.objects.get_or_create(name=r.json().get('Writer'))[0]
        stars = r.json().get('Actors').split(', ')
        alist = []
        for a in stars:
            if a not in Actor.objects.all():
                actor = Actor.objects.get_or_create(name=a)[0]
                alist.append(actor)
                actor.save()

        j = r.json()

        if j.get('Rated') == 'G':
            rated = 1
        elif j.get('Rated') == 'PG':
            rated = 2
        elif j.get('Rated') == 'PG-13':
            rated = 3
        else:
            rated = 4

        new_movie = Movie.objects.get_or_create(name=r.json().get('Title'), year=r.json().get('Year'),
                                         director=d, writer=w, rated=rated, imdbId=r.json().get('imdbID'))[0]

        new_movie.poster = 'http://image.tmdb.org/t/p/w300/{0}'.format(poster_url)
        template_poster = 'http://image.tmdb.org/t/p/w300/{0}'.format(poster_url)

        new_movie.save()
        for a in alist:
            new_movie.actors.add(a)
        new_movie.save()
        if search_query is not None:
            r = requests.get('http://www.omdbapi.com/?t={0}&y=&plot=short&r=json'.format(search_query.replace(' ', '+')))
        else:
            r = requests.get('http://www.omdbapi.com/?i={0}&plot=short&r=json'.format(imdb))
        return render(request, 'movies/movie_summary.html', {'movie': r.json, 'poster': template_poster, 'exists_in_library': False})

    r = requests.get('http://www.omdbapi.com/?t={0}&y=&plot=short&r=json'.format(m.name.replace(' ', '+')))

    try:
        if not request.user.is_authenticated:
            exists_in_library = False
        else:
            # if request.user.is_anonymous:
            #     exists_in_library = False
            # else:
            exists_in_library = request.user.movie_set.get(name=r.json().get('Title')).name
    except Movie.DoesNotExist:
        exists_in_library = False

    return render(request, 'movies/movie_summary.html', {'movie': r.json, 'exists_in_library': exists_in_library})

def search(request):
    search_query = request.POST.get('search_query')

    r = requests.get('http://www.omdbapi.com/?t={0}&y=&plot=short&r=json'.format(search_query.replace(' ', '+')))

    try:
        exists_in_library = Movie.objects.get(name=r.json().get('Title')).name
    except Movie.DoesNotExist:
        exists_in_library = False
    if r.json().get('Response') == 'True':
        return movie_summary(request, r.json().get('imdbID'), search_query)
    else:
        return render(request, 'movies/index.html', {'SearchError': 'Movie not found!'})

def add_to_library(request, id):
    # FIXME Grab any extra fields we will need in the future and save
    # so we don't have to make extra requests
    m = Movie.objects.get(imdbId=id)

    if request.user not in m.users.all():
        m.users.add(request.user)
    m.save()

    return redirect('/movie_list')

def remove_from_library(request, id):
    removeme = request.user.movie_set.get(imdbId=id)
    request.user.movie_set.remove(removeme)

    return redirect('/movie_list')

def sign_out(request):
    logout(request)
    return redirect('/')

@login_required
def pagination(request):
    movie_list = themovies = request.user.movie_set.all()
    paginator = Paginator(movie_list, 10)

    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        movies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        movies = paginator.page(paginator.num_pages)

    for movie in themovies:
        r = requests.get('http://www.omdbapi.com/?t={0}&y=&plot=short&r=json'.format(movie.name.replace(' ', '+')))
        # movie.poster = r.json().get('Poster')
        movie.imdbId = r.json().get('imdbID')
        movie.save()

    return render_to_response('movies/movie_list.html', {"movies": movies})

# def test403(request):
#     r = requests.get('http://www.omdbapi.com/?t=Cars&y=&plot=short&r=json')
#     return render_to_response('movies/test403.html', {'json': r.json()})
