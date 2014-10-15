from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict

from models import Blob

# passed into page responses used for static variables that might change in the future such as the site address
script_args = {}
script_args['site_url'] = 'http%3A//dylanzingler.com'
script_args['pages'] = ['resume','mobilewebpractice', 'storage', 'blobs']
# CSS them for the site
script_args['theme'] = 'a'

def Create_test_user_group(test_users):
    root = Blob()
    root.name = "user"
    root.save()
    
    for user in range(test_users):
        usr = Blob()
        usr.name = "user_" + str(user)
        usr.blobject = root
        usr.save()

def Create_test_profile_group(test_users):
    root = Blob()
    root.name = "profile"
    root.save()
    
    user_root = Blob.objects.filter(parent=None, name="user")
    users = Blob.objects.filter(parent=user_root)
    print user_root
    print users
    
    for user in range(test_users):
        usr = Blob()
        usr.name = "profile_" + str(user)
        usr.blobject = root
        usr.save()




def blobs(request):
    
    # Create a few users
    Create_test_user_group(3)
    Create_test_profile_group(3)
    
    
    # All Blobs
    script_args["blobs"] = Blob.objects.all()
        
    
    return render_to_response("blobs/blobs.html", script_args)


def hangers(request):
    
    
    # All Blobs
    script_args["hangers"] = Blob.objects.all()
        
    
    return render_to_response("blobs/hangers.html", script_args)




