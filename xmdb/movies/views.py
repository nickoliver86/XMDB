from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic
# Create your views here.

class IndexView(generic.ListView):
    #template_name = 'movies/index.html'
    def get_queryset(self):
        """Return the last five published questions."""
        return "hey"


def IndexTest(request):
    return render(request, 'index.html')
