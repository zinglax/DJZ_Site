from django.db import models

####################################################
## BLOB: Like Object in Java, this class is the
## building block for for all other objects in this
## site. 
## Example: A Blob_User might have a Blob_Email
## or a Blob_Profile-Pic containted in it that each
## have their parent set to a Blob-User
####################################################
class Blob(models.Model):
    # Name of Blob
    name = models.CharField(max_length=150) 

    # Description of Blob
    description = models.CharField(max_length=500, blank=True, null=True) 
    
    # Parent of Blob 
    parent = models.ForeignKey('self', blank=True, null=True,on_delete=models.SET_NULL, )

    # Barcode Label ex. DJZ128
    barcode = models.CharField(max_length=150)

    # Number of times this item has 
    hit_count = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):        
        return self.name  