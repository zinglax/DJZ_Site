from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict

# passed into page responses used for static variables that might change in the future such as the site address
script_args = {}
script_args['site_url'] = 'http%3A//dylanzingler.com'
script_args['pages'] = ['resume','mobilewebpractice', 'storage', 'blobs']
# CSS them for the site
script_args['theme'] = 'a'

def blobs(request):
    
    # All Blobs
    return render_to_response("blobs/blobs.html", script_args)