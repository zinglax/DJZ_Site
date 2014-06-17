from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict

# For Navigation
pages = ['resume','mobilewebpractice', 'storage']


def home(request):
  return render_to_response("storage/home.html",{'pages':pages})
