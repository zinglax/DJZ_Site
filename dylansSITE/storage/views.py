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
        return render_to_response("storage/home.html",{})
    else:
        return redirect('/storage/' + qr + "/")
        

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
      
          
      return render_to_response("storage/item.html",{'item':I})
    else:
      print 'this is not a post request'
    
    
    item = get_or_none(Item, barcode=bar_code)
    if (item == None):
        args = {}
        args['barcode'] = bar_code
        args.update(csrf(request))
        return render_to_response("storage/add.html",args)
    else:
        return render_to_response("storage/item.html",{'item':item})        

def search(request):
    #areas = Item.objects.all().filter(parent_item__isnull=True)
    areas = Item.objects.all()
    return render_to_response("storage/search.html",{'areas':areas})

def item(request, bar_code):
    item = get_or_none(Item, barcode=bar_code)
    if (item == None):
        
        return redirect('/storage/add/' + bar_code + "/")
        #return render_to_response("storage/add.html",{})
    else:
        return render_to_response("storage/item.html",{'item':item})
  
  
      
