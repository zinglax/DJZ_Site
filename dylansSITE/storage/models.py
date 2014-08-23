from django.db import models

# Item, can contain other items
class Item(models.Model):
    # Name of Item/Container
    name = models.CharField(max_length=150) 

    # Description of item or container
    description = models.CharField(max_length=500, blank=True, null=True) 
    
    # Where the item or container is stored in 
    parent = models.ForeignKey('self', blank=True, null=True,on_delete=models.SET_NULL, )

    # Barcode Label ex. DJZ128
    barcode = models.CharField(max_length=150)

    # Number of times this item has 
    hit_count = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):        
        return self.name    
    
    
