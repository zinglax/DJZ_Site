from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response


from models import *
from django.conf import settings



def home(request):
  
  return render_to_response("home/new_page.html", {})
