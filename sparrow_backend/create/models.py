from django.db import models
import uuid
from nested_lookup import nested_lookup
import os

# Create your models here.
class Layout(models.Model):
    
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    format = models.JSONField()
    title = models.CharField(max_length=100,blank=True,null=True)
    gsheetId = models.CharField(max_length=100,blank=True,null=True)
    train = models.JSONField(blank=True,null=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return None


