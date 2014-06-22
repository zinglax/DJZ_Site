from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500, blank=True, null=True)
    picture = models.ImageField(upload_to='item_photos', blank=True, null=True)  
    date_created = models.DateTimeField(auto_now_add=True)
    last_scanned = models.DateTimeField(blank=True, null=True)
    label_text = models.CharField(max_length=80, blank=True, null=True)
    needs_label = models.BooleanField()
    parent_item = models.ForeignKey('self', blank=True, null=True,on_delete=models.SET_NULL, )
    is_area = models.BooleanField()
    
    def __unicode__(self):        
        return self.name    
    
    
