from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from forms import ItemForm
from django.core.context_processors import csrf


def storage(request):
  return render_to_response("storage/home.html",{})

def add(request):
  if request.POST:
    
    print request.POST["name"]
    print request.POST["description"]
    print request.POST["labeltext"]
    
    print request.POST["printlabel"]
    
    print request.POST
    
    form = ItemForm(request.POST)
    
    return HttpResponseRedirect("storage/home.html")
  else:
    print 'this is not a post request'
  
  args = {}
  args.update(csrf(request))
  return render_to_response("storage/add.html",args)

def search(request):
  return render_to_response("storage/search.html",{})

def prints(request):
  return render_to_response("storage/prints.html",{})

def item(request, item_id=1):
  
  # Item.objects.get(itemNum = item_number) HINT
  item = Item.objects.get(id=item_id)
  
  return render_to_response("storage/item.html",{'item':item})