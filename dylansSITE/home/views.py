from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict

from home.forms import UserForm, UserProfileForm

from django.contrib.auth import authenticate, login

from django.core.context_processors import csrf

from django.contrib.auth import logout

# payments
import stripe

from os import listdir
from os.path import isfile, join
from models import *
from django.conf import settings
from dylansSITE.settings import PATH_TO_FILE

from random import randint

from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt

import storage.views as StorageViews

import re

# List of navigable pages, add new pages to this list for nav pannel
pages = ['storage','images','photobooth', 'voice', 'payments']
script_args = {}
script_args['pages'] = pages

# Random theme 
themes = ['a','b','c','d','e','f']
#script_args['theme'] = themes[randint(0, len(themes)-1)]

def home(request):
  context = RequestContext(request)  
  script_args['theme'] = themes[randint(0, len(themes)-1)]

  # Favicon
  favicon = 'images/favicon.ico'
  script_args['favicon'] = favicon
  
  # Resume
  script_args['resume'] = 'Resume.pdf'
    
  return render_to_response("home/home.html", script_args, context)

def photobooth(request):
  
  print request
  datauri = request.POST.get('canvasData', '')
  
  
  #imgstr = re.search(r'base64,(.*)', datauri).group(1)
  
  #output = open('output.png', 'wb')
  
  #output.write(imgstr.decode('base64'))
  
  #output.close()  
  
  
  return render_to_response("home/index.html", script_args)

def voice(request):
  return render_to_response("home/voice.html", script_args)


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


def register(request):
  # Like before, get the request's context.
  context = RequestContext(request)

  # A boolean value for telling the template whether the registration was successful.
  # Set to False initially. Code changes value to True when registration succeeds.
  registered = False

  # If it's a HTTP POST, we're interested in processing form data.
  if request.method == 'POST':
    # Attempt to grab information from the raw form information.
    # Note that we make use of both UserForm and UserProfileForm.
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileForm(data=request.POST)

    # If the two forms are valid...
    if user_form.is_valid() and profile_form.is_valid():
      # Save the user's form data to the database.
      user = user_form.save()

      # Now we hash the password with the set_password method.
      # Once hashed, we can update the user object.
      user.set_password(user.password)
      user.save()

      # Now sort out the UserProfile instance.
      # Since we need to set the user attribute ourselves, we set commit=False.
      # This delays saving the model until we're ready to avoid integrity problems.
      profile = profile_form.save(commit=False)
      profile.user = user

      # Did the user provide a profile picture?
      # If so, we need to get it from the input form and put it in the UserProfile model.
      if 'picture' in request.FILES:
        profile.picture = request.FILES['picture']

      # Now we save the UserProfile model instance.
      profile.save()

      # Update our variable to tell the template registration was successful.
      registered = True

    # Invalid form or forms - mistakes or something else?
    # Print problems to the terminal.
    # They'll also be shown to the user.
    else:
      print user_form.errors, profile_form.errors

  # Not a HTTP POST, so we render our form using two ModelForm instances.
  # These forms will be blank, ready for user input.
  else:
    user_form = UserForm()
    profile_form = UserProfileForm()

  # Render the template depending on the context.
  return render_to_response(
    'home/register.html',
    {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
    context)

def user_login(request):
  # Like before, obtain the context for the user's request.
  context = RequestContext(request)

  # If the request is a HTTP POST, try to pull out the relevant information.
  if request.method == 'POST':
    # Gather the username and password provided by the user.
    # This information is obtained from the login form.
    username = request.POST['username']
    password = request.POST['password']

    # Use Django's machinery to attempt to see if the username/password
    # combination is valid - a User object is returned if it is.
    user = authenticate(username=username, password=password)

    # If we have a User object, the details are correct.
    # If None (Python's way of representing the absence of a value), no user
    # with matching credentials was found.
    if user:
      # Is the account active? It could have been disabled.
      if user.is_active:
        # If the account is valid and active, we can log the user in.
        # We'll send the user back to the homepage.
        login(request, user)
        return HttpResponseRedirect('/')
      else:
        # An inactive account was used - no logging in!
        return HttpResponse("Your Rango account is disabled.")
    else:
      # Bad login details were provided. So we can't log the user in.
      print "Invalid login details: {0}, {1}".format(username, password)
      return HttpResponse("Invalid login details supplied.")

  # The request is not a HTTP POST, so display the login form.
  # This scenario would most likely be a HTTP GET.
  else:
    # No context variables to pass to the template system, hence the
    # blank dictionary object...
    return render_to_response('home/login.html', {}, context)
  
@login_required
def restricted(request):
  return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request):
  # Since we know the user is logged in, we can now just log them out.
  logout(request)

  # Take the user back to the homepage.
  return HttpResponseRedirect('/')

def custom_404(request):
  return render_to_response('home/404.html', RequestContext(request))

def custom_500(request):
  return render_to_response('home/500.html', RequestContext(request))



@csrf_exempt
def payments(request):
  
  context = RequestContext(request)
  
  
  # Set your secret key: remember to change this to your live secret key in production
  # See your keys here https://dashboard.stripe.com/account/apikeys
  stripe.api_key = "sk_test_yw7IZbUI1cFgnCD7balmgyu9"
  
  
  # TEST
  # Secret: sk_test_yw7IZbUI1cFgnCD7balmgyu9  
  # Pubish: pk_test_wGdOnYU7xw3DBYvNXQXG6gxK
  
  # LIVE
  # Secret: sk_live_uzSgp2cqSeVMCYVfRiJIat55
  # Publish: pk_live_NMedpGOUK9zEs5SRyv5RHHjw
  
  if request.method == 'POST':
    # Get the credit card details submitted by the form
    token = request.POST['stripeToken']
    
    # Create the charge on Stripe's servers - this will charge the user's card
    try:
      charge = stripe.Charge.create(
          amount=1599, # amount in cents, again
          currency="usd",
          source=token,
          description="TEST CHARGE FROM DYLAN ZINGLER"
      )
      #return render_to_response('home/payments.html', script_args, context)
    except stripe.error.CardError, e:
      # The card has been declined
      pass
  
  
  
  return render_to_response('home/payments.html', script_args, context)


