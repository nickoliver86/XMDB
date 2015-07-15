from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from movies.models import *
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