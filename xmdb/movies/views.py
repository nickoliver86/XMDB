from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from movies.models import *
import requests
# Create your views here.

class IndexView(generic.ListView):
    #template_name = 'movies/index.html'
    def get_queryset(self):
        """Return the last five published questions."""
        return "hey"


def IndexTest(request):
    return render(request, 'movies/index.html')

def signin(request):
    return render(request, 'movies/signin.html')

def UserSignUp(request):
    if request.POST.get('password1') != request.POST.get('password2'):
        return render (request, 'movies/index.html', {'ErrorMessage':'Your passwords must match'})
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password1')
    u = User()
    u.username = username
    u.email = email
    u.password = password
    u.save()
    return signin(request)

def MovieList(request):
    themovies = Movie.objects.all()
    #The following retrieves movie posters from api for movies added through admin console
    for movie in themovies:
        r = requests.get('http://www.omdbapi.com/?t={0}&y=&plot=short&r=json'.format(movie.name.replace(' ', '+')))
        movie.poster = r.json().get('Poster')
        movie.imdbId = r.json().get('imdbID')
        movie.save()
    return render(request, 'movies/movie_list.html', {"movies": themovies})

def MovieSummary(request, movie_id):
    m = Movie.objects.get(id=movie_id)
    r = requests.get('http://www.omdbapi.com/?t={0}&y=&plot=short&r=json'.format(m.name.replace(' ', '+')))
    try:
        exists_in_library = Movie.objects.get(name=r.json().get('Title')).name
    except Movie.DoesNotExist:
        exists_in_library = False
    return render(request, 'movies/movie_summary.html', {'movie': r.json, 'exists_in_library': exists_in_library})

def Search(request):
    search_query = request.POST.get('search_query')
    r = requests.get('http://www.omdbapi.com/?t={0}&y=&plot=short&r=json'.format(search_query.replace(' ', '+')))
    try:
        exists_in_library = Movie.objects.get(name=r.json().get('Title')).name
    except Movie.DoesNotExist:
        exists_in_library = False
    if r.json().get('Response') == 'True':
        return render(request, 'movies/movie_summary.html', {'movie': r.json, 'exists_in_library': exists_in_library})
    else:
        return render(request, 'movies/index.html', {'SearchError':'Movie not found!'})

def AddToLibrary(request, id):

    r = requests.get('http://www.omdbapi.com/?i={0}&plot=short&r=json'.format(id))
    j = r.json()
    d = Director.objects.create(name=j.get('Director'))
    d.save()
    w = Writer.objects.create(name=j.get('Writer'))
    w.save()
    p = j.get('Poster')
    stars = j.get('Actors').split(', ')
    alist = []
    for a in stars:
        actor = Actor.objects.create(name=a)
        alist.append(actor)
        actor.save()

    if j.get('Rated') == 'G':
        rated = 1
    elif j.get('Rated') == 'PG':
        rated = 2
    elif j.get('Rated') == 'PG-13':
        rated = 3
    else:
        rated = 4

    m = Movie.objects.create(name=j.get('Title'), year=j.get('Year'),
                             director=d, writer=w, rated=rated, poster=p, imdbId=j.get('imdbId'))
    m.save()
    for a in alist:
        m.actors.add(a)
    m.save()
    return redirect('/movie_list')

def RemoveFromLibrary(request, id):
    deleteme = Movie.objects.get(imdbId=id)
    deleteme.delete()
    return redirect('/movie_list')

