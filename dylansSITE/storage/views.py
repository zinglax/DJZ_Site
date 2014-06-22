from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from forms import ItemForm
from models import Item
from django.core.context_processors import csrf

from dylansSITE.settings import STATIC_ROOT

def storage(request):
  return render_to_response("storage/home.html",{})

def add(request):
  if request.POST:
    I = Item()
    info = request.POST
    I.name = info["name"]
    
    
    if (request.POST.get('printlabel', False)):  
      I.description = info["description"]
      
    if (request.POST.get('printlabel', False)):  
      I.needs_label = True
      
    I.save()
    print I.description
    return render_to_response("storage/search.html")
  else:
    print 'this is not a post request'
  
  args = {}
  args.update(csrf(request))
  return render_to_response("storage/add.html",args)

def search(request):
  areas = Item.objects.all().filter(parent_item__isnull=True)
  
  return render_to_response("storage/search.html",{'areas':areas})


def prints(request):
  labels = Item.objects.all().filter(needs_label=True)
  print labels
  return render_to_response("storage/prints.html",{'labels':labels})

def item(request, item_id=1):
  
  # Item.objects.get(itemNum = item_number) HINT
  item = Item.objects.get(id=item_id)
  
  return render_to_response("storage/item.html",{'item':item})