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
from django.db.models import Q
import djqscsv

# passed into page responses used for static variables that might change in the future such as the site address
script_args = {}
script_args['site_url'] = 'http%3A//dylanzingler.com'

# CSS them for the site
script_args['theme'] = 'a'

def get_or_none(model, **kwargs):
    # Gets object or returns none if not found
    # EX. foo = get_or_none(Item, barcode=DJZ48)
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    
def storage(request):   
    
    # Items with out a parent
    script_args['top'] = Item.objects.filter(parent=None)
    
    # All Items
    script_args["all"] = Item.objects.all()
    
    # Gets the qrcode value    
    qr = request.GET.get('qr', '')
    
    # Nothing Scanned
    if (qr == ''):
        return render_to_response("storage/home.html",script_args)
    
    # Redirects to the items page
    else:
        return redirect('/storage/' + qr + "/")


def update(request):
    # Gets the qrcode value    
    qr = request.GET.get('qr', '')
    
    # Nothing Scanned    
    if (qr == ''):
        return render_to_response("storage/update.html",script_args)
    
    # Redirect to the items update mode
    else:
        return redirect('/storage/u/' + qr + "/")
    
def update_item(request, bar_code):
    
    # gets the parent item
    parent_item = get_or_none(Item, barcode=bar_code)
    
    # If parent item is not in system got to the add process
    if (parent_item == None):     
            return redirect('/storage/add/' + bar_code + "/")    
    
    # Gets the qrcode value
    qr = request.GET.get('qr', '')
    
    print "#### ITEM UPDATING: " + bar_code
    print "#### SCANNED CODE: " + qr
    
    # Nothing scanned
    if (qr == ''):
        # Loads barcode scanning app
        response = HttpResponse("", status=302)
        response['Location'] = 'pic2shop://scan?callback='+ script_args['site_url'] + '/storage/u/' + bar_code + "/"       
        return response  
    
    # Barcode scanned is the same as the parent (STOP SCANNING)
    elif (qr == bar_code):
        return render_to_response("storage/search.html",script_args)
    
    # Barcode scanned is not the same as the parent (UPDATE & CONTINUE SCANNING)
    else:
        # Gets the scanned item
        item = get_or_none(Item, barcode=qr)        
        
        # if the scanned item does not exist redirect to add page
        if (item == None):     
                return redirect('/storage/add/' + qr + "/")    
        
        # Updates the scanned items parent 
        item.parent = parent_item
        item.save()
        
        # Loads Barcode scanning app again for the next barcode to be scanned
        response = HttpResponse("", status=302)
        response['Location'] = 'pic2shop://scan?callback='+ script_args['site_url'] + '/storage/u/' + bar_code + "/"       
        return response  
    
        

def add(request, bar_code):
    print '### BARCODE IS: ' + bar_code
    if request.POST:
        
        # Creating item object from form values
        I = Item()
        info = request.POST
        I.name = info["name"]
        I.barcode = bar_code
        if (request.POST.get('description', False)):  
            I.description = info["description"]
        I.save()
        
        script_args['item'] = I
        
        # Goes to item page
        return render_to_response("storage/item.html",script_args)
    else:
        print 'this is not a post request'
    
    
    item = get_or_none(Item, barcode=bar_code)
    
    # Item does not exist go to the add page
    if (item == None):
        
        script_args['barcode'] = bar_code
        script_args.update(csrf(request))
        return render_to_response("storage/add.html",script_args)
    
    # Item already exists, goes to item page
    else:
        script_args['item'] = item
        return render_to_response("storage/item.html",script_args)        

def search(request):

    if "search" in request.GET:
        search = request.GET["search"]
        
        
        # Get the items that have the search in the name and or description
        script_args['results'] = Item.objects.all().filter((Q(name__icontains=search)|Q(description__icontains=search))| (Q(name__icontains=search)&Q(description__icontains=search)))
    else:
        script_args['results'] = False
        
    script_args['areas'] = Item.objects.all()
    return render_to_response("storage/search.html",script_args)

def item(request, bar_code):
    # Gets the item associated with the specific barcode
    item = get_or_none(Item, barcode=bar_code)
    
    # The item does not exist yet, goes to the add page
    if (item == None):
        return redirect('/storage/add/' + bar_code + "/")
    # Go to the specific items page
    else:
        
        # Used For Deletion
        if request.GET:
            yesno = request.GET["yesno"]
            if yesno == 'yes':
                
                children = Item.objects.all().filter(parent=item)
                for child in children:
                    child.parent = None
                    
                item.delete()
                
                
                return render_to_response("storage/home.html",script_args)
            else:
                return redirect('/storage/' + bar_code + "/")
                
        
        # Used For updating
        if request.POST:
            info = request.POST
            item.name = info["name"]
            if (request.POST.get('description', False)):  
                item.description = info["description"]
            item.save()            
            return redirect('/storage/' + bar_code + "/")
        
        
        script_args['children'] = Item.objects.filter(parent=item)
        
        script_args['item'] = item
        script_args.update(csrf(request))        
        return render_to_response("storage/item.html",script_args)
  
def export(request):
    qs = Item.objects.all()
    return djqscsv.render_to_csv_response(qs)

def about(request):
    return render_to_response("storage/about.html",script_args)
    
