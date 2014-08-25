from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from forms import ItemForm
from models import Item
from django.core.context_processors import csrf
from django.shortcuts import redirect
from dylansSITE.settings import STATIC_ROOT

# passed into page responses used for static variables that might change in the future such as the site address
script_args = {}
script_args['site_url'] = 'http%3A//192.168.1.17:8001'

def get_or_none(model, **kwargs):
    # Gets object or returns none if not found
    # EX. foo = get_or_none(Item, barcode=DJZ48)
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    
def storage(request):   
    qr = request.GET.get('qr', '')
    
    if (qr == ''):
        return render_to_response("storage/home.html",script_args)
    else:
        return redirect('/storage/' + qr + "/")


def update(request):
    qr = request.GET.get('qr', '')
    
    if (qr == ''):
        return render_to_response("storage/update.html",script_args)
    else:
        return redirect('/storage/u/' + qr + "/")
        
        #response = HttpResponse("", status=302)
        #response['Location'] = 'pic2shop://scan?callback='+ script_args['site_url'] + '/storage/update/' + qr + "/" 
        #return response  
    
def update_item(request, bar_code):
    qr = request.GET.get('qr', '')
    
    print "#### ITEM UPDATING: " + bar_code
    print "#### SCANNED CODE: " + qr
    
    # Nothing scanned
    if (qr == ''):
        response = HttpResponse("", status=302)
        response['Location'] = 'pic2shop://scan?callback='+ script_args['site_url'] + '/storage/u/' + bar_code + "/"       
        return response  
    
    # Barcode scanned is the same as the parent (STOP SCANNING)
    elif (qr == bar_code):
        return render_to_response("storage/update.html",script_args)
    
    # Barcode scanned is not the same as the parent (UPDATE & CONTINUE SCANNING)
    else:
        response = HttpResponse("", status=302)
        response['Location'] = 'pic2shop://scan?callback='+ script_args['site_url'] + '/storage/u/' + bar_code + "/"       
        return response  
    
        

def add(request, bar_code):
    print '### BARCODE IS: ' + bar_code
    if request.POST:
      I = Item()
      info = request.POST
      I.name = info["name"]
      I.barcode = bar_code
      if (request.POST.get('description', False)):  
        I.description = info["description"]
      I.save()
      
      script_args['item'] = I
          
      return render_to_response("storage/item.html",script_args)
    else:
      print 'this is not a post request'
    
    
    item = get_or_none(Item, barcode=bar_code)
    if (item == None):
        args = {}
        args['barcode'] = bar_code
        args.update(csrf(request))
        return render_to_response("storage/add.html",args)
    else:
        script_args['item'] = item
        
        return render_to_response("storage/item.html",script_args)        

def search(request):
    #areas = Item.objects.all().filter(parent_item__isnull=True)
    script_args['areas'] = Item.objects.all()
    return render_to_response("storage/search.html",script_args)

def item(request, bar_code):
    item = get_or_none(Item, barcode=bar_code)
    if (item == None):
        
        return redirect('/storage/add/' + bar_code + "/")
        #return render_to_response("storage/add.html",{})
    else:
        script_args['item'] = item        
        return render_to_response("storage/item.html",script_args)
  
  
