from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict

from models import *

# passed into page responses used for static variables that might change in the future such as the site address
script_args = {}
script_args['site_url'] = 'http%3A//dylanzingler.com'
script_args['pages'] = ['resume','mobilewebpractice', 'storage', 'blobs']
# CSS them for the site
script_args['theme'] = 'e'

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

def create_hanger(name, hung_on=None):
    hanger = Hanger()
    hanger.name = name
    hanger.hung_on = hung_on
    return hanger

def create_data_hanger(tp, data, hung_on=None):
    
    hanger = None
    
    if tp == "str" or tp == "string" or tp == "String":
        hanger = Str_Hanger()
        hanger.data = data
        hanger.hung_on = hung_on
        
    elif tp == "int" or tp == "integer" or tp == "Integer":
        hanger = Int_Hanger()
        hanger.data = data
        hanger.hung_on = hung_on        
        
    elif tp == "boolean" or tp == "bool" or tp == "Boolean":
        hanger = Boolean_Hanger()
        hanger.data = data
        hanger.hung_on = hung_on        
        
    elif tp == "email" or tp == "Email" or tp == "e-mail":
        hanger = Email_Hanger()
        hanger.data = data
        hanger.hung_on = hung_on
    
    if hanger == None:
        print "Error: Could not find type of hanger you were trying to create"
        return
    return hanger


def create_hangers_object(name, features, hung_on=None):
    named_hanger = create_hanger(name, hung_on)
    named_hanger.save()
    
    for f in features:
        data_label_hanger = create_hanger(f[0], named_hanger)
        data_label_hanger.save()
        data_hanger = create_data_hanger(f[1], f[2], data_label_hanger)
        data_hanger.save()

    return named_hanger


####################################################
## blobs page
def blobs(request):
    
    # Create a few users
    Create_test_user_group(3)
    Create_test_profile_group(3)
    
    
    # All Blobs
    script_args["blobs"] = Blob.objects.all()
        
    
    return render_to_response("blobs/blobs.html", script_args)


####################################################
## hangers page
def hangers(request):
    
    strings = create_hanger("Strings")
    #strings = Hanger.objects.get(name="Strings")
    string1 = create_data_hanger("str", "string1", strings)
    string1.save()
    
    features = []
    feature = ["nipple", "string","It's a tittly bit nipply out..."]
    features.append(feature)
    
    create_hangers_object("Boob", features)
    
    print strings
    # All Blobs
    script_args["hangers"] = Hanger.objects.all()
    script_args["strings"] = Str_Hanger.objects.all()
    print script_args["strings"]
    print script_args["hangers"]
    
    
    return render_to_response("blobs/hangers.html", script_args)



           
