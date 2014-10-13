from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict


from models import *
from django.conf import settings
from dylansSITE.settings import PATH_TO_FILE

import storage.views as StorageViews

pages = ['resume','mobilewebpractice', 'storage', 'blobs']

def home(request):
  print PATH_TO_FILE + "/media/site_pictures/D.jpg"
  logo = "/media/site_pictures/D.jpg"
  return render_to_response("home/home.html", {'logo':logo, 'pages':pages})

def mobilewebpractice(request):
  return render_to_response("home/mobilewebpractice.html", {'pages':pages})

def resume(request):
  return render_to_response("home/resume.html",{'pages':pages})


def serve_pdf(request):
    #pdf_data = magically_create_pdf()

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="/media/ITresmue.pdf"'
    response['X-Sendfile'] = "/media/ITresmue.pdf"
    
    return response
  
def storage(request):
  return StorageViews.storage(request);