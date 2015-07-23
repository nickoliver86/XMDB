from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.models import User
from movies.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import requests
from django import forms, views
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

class IndexView(generic.ListView):
    #template_name = 'movies/index.html'
    def get_queryset(self):
        """Return the last five published questions."""
        return "hey"

# FIXME Regarding naming conventions, best to follow pep-8.  
# methods should be lower case and words separated by underscores
# Classes can be first letter capitalized (not camel case), no underscores

def index_test(request):
    #import pdb; pdb.set_trace()
    return render(request, 'movies/index.html')

def sign_in(request):
    # FIXME What if user is already logged in?
    if request.method == 'POST':
        un = request.POST.get('username')
        pw = request.POST.get('password')
        user = authenticate(username=un, password=pw)
        #user = User.objects.get(username=un, password=pw)
        #import pdb; pdb.set_trace()
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('movies:IndexTest'))
            else:
                return HttpResponseRedirect("Your account is disabled.")
        else:
            print('Invalid login details: {0}, {1}'.format(un, pw))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'movies/signin.html', {})

def user_sign_up(request):
    # This is inefficient and dangerous!  Never take input directly from the 
    # request and store directly in the database!!!  
    # FIXME Use a ModelForm here
    # if request.POST.get('password1') != request.POST.get('password2'):
    #     return render(request, 'movies/index.html', {'ErrorMessage':'Your passwords must match'})
    # username = request.POST.get('username')
    # email = request.POST.get('email')
    # password = request.POST.get('password1')
    # u = User.objects.create_user(username, email, password)
    # u.save()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("")
        else:
            form = UserCreationForm()
    return render(request, "movies/index.html")

@login_required
def movie_list(request):
    #themovies = Movie.objects.all()
    # liaison = UserList.objects.get(user=request.user)
    themovies = request.user.movie_set.all()
    #The following retrieves movie posters from api for movies added through admin console

    # FIXME We're making requests for every single movie every time we
    # display the movie list! Why don't we store the meta data in the database
    # and only grab the stuff we need

    # FIXME Add pagination, movie list may get long
    for movie in themovies:
        r = requests.get('http://www.omdbapi.com/?t={0}&y=&plot=short&r=json'.format(movie.name.replace(' ', '+')))
        movie.poster = r.json().get('Poster')
        movie.imdbId = r.json().get('imdbID')
        movie.save()
    return render(request, 'movies/movie_list.html', {"movies": themovies})

def movie_summary(request, movie_id):
    #m = Movie.objects.get(id=movie_id)
    #movielist = UserList.objects.get(user=request.user).movies
    movielist = request.user.movie_set.all()
    m = movielist.get(id=movie_id)
    # for movie in movielist:
    #     if movie.id == movie_id:
    #         m = movie
    #         break
    # FIXME When we grab this stuff from the database, why do we need to make another
    # request to the omdbapi?  Why can't we just ensure that when we store the movie
    # in the database that it's fully parsed so I don't have to call the api again?

    r = requests.get('http://www.omdbapi.com/?t={0}&y=&plot=short&r=json'.format(m.name.replace(' ', '+')))

    try:
        exists_in_library = Movie.objects.get(name=r.json().get('Title')).name
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
        return render(request, 'movies/movie_summary.html', {'movie': r.json, 'exists_in_library': exists_in_library})
    else:
        return render(request, 'movies/index.html', {'SearchError':'Movie not found!'})

def add_to_library(request, id):
    # FIXME Grab any extra fields we will need in the future and save
    # so we don't have to make extra requests
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

    m = Movie.objects.get_or_create(name=j.get('Title'), year=j.get('Year'),
                             director=d, writer=w, rated=rated, poster=p,
                             imdbId=j.get('imdbID'))[0]
    m.users.add(request.user)
    m.save()
    for a in alist:
        m.actors.add(a)
    m.save()

    return redirect('/movie_list')

def remove_from_library(request, id):
    deleteme = Movie.objects.get(imdbId=id)
    deleteme.delete()
    return redirect('/movie_list')

def sign_out(request):
    logout(request)
    return redirect('/')

