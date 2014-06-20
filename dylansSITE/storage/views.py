from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from forms import ItemForm


def storage(request):
  return render_to_response("storage/home.html",{})

def add(request):
  if request.POST:
    form = ItemForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect("storage/home.html")
  else:
    form = ItemForm()
    
  args = {}
  
  args['form'] = form
  
  return render_to_response("storage/add.html",args)

def search(request):
  return render_to_response("storage/search.html",{})

def prints(request):
  return render_to_response("storage/prints.html",{})

def item(request, item_id=1):
  
  # Item.objects.get(itemNum = item_number) HINT
  item = Item.objects.get(id=item_id)
  
  return render_to_response("storage/item.html",{'item':item})