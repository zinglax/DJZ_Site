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

from random import randint

import storage.views as StorageViews

# List of navigable pages, add new pages to this list for nav pannel
pages = ['storage','images','photobooth']
script_args = {}
script_args['pages'] = pages

# Random theme 
themes = ['a','b','c','d','e','f']
#script_args['theme'] = themes[randint(0, len(themes)-1)]

def home(request):
  
  script_args['theme'] = themes[randint(0, len(themes)-1)]

  # Favicon
  favicon = 'images/favicon.ico'
  script_args['favicon'] = favicon
  
  # Resume
  script_args['resume'] = 'Resume.pdf'
  
  return render_to_response("home/home.html", script_args)

def photobooth(request):
  
  return render_to_response("home/index.html", script_args)

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

#def mobilewebpractice(request):
  #return render_to_response("home/mobilewebpractice.html", script_args)


  
def storage(request):
  return StorageViews.storage(request);