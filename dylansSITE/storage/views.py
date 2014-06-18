from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict

# For Navigation
pages = ['add','search']


def storage(request):
  return render_to_response("storage/home.html",{'pages':pages})

def add(request):
  return render_to_response("storage/add.html",{'pages':pages})

def search(request):
  return render_to_response("storage/search.html",{'pages':pages})