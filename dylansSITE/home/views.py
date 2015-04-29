from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict


from os import listdir
from os.path import isfile, join
from models import *
from django.conf import settings
from dylansSITE.settings import PATH_TO_FILE

import storage.views as StorageViews

# List of navigable pages, add new pages to this list for nav pannel
pages = ['resume','mobilewebpractice', 'storage', 'blobs','images']
script_args = {}
script_args['pages'] = pages

def home(request):
  return render_to_response("home/home.html", script_args)

def images(request):
  imagefolder = PATH_TO_FILE + '/static/images'
  
  # Files in image folder
  onlyfiles = [ f for f in listdir(imagefolder) if isfile(join(imagefolder,f)) ]  
  
  # Finding the images
  img_files = []
  for f in onlyfiles:
    print f
    if (f[-4:] == ".gif") or (f[-4:] == ".jpg") or (f[-4:] == ".png"):
      f = "images/" + f
      img_files.append(f)
  print img_files
  
  script_args['img_files'] = img_files
  return render_to_response("home/images.html", script_args)

def mobilewebpractice(request):
  return render_to_response("home/mobilewebpractice.html", script_args)

def resume(request):
  
  
  #response = HttpResponse(mimetype='application/force-download')
  #response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
  #response['X-Sendfile'] = smart_str(path_to_file)  
  
  
  
  
  return render_to_response("home/Resume.html",script_args)


def serve_pdf(request):
    #pdf_data = magically_create_pdf()

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="/media/ITresmue.pdf"'
    response['X-Sendfile'] = "/media/ITresmue.pdf"
    
    return response
  
def storage(request):
  return StorageViews.storage(request);