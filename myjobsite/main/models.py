from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User





class Jobs(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    posted_by = models.CharField(max_length=100)
    posted_on = models.DateField()

class added_jobs():
    
    email = models.EmailField(max_length=254)
    id=models.AutoField(auto_created = True)
    def __init__(self,email):
        self.email=email
    class Meta:
        unique_together = (('email', 'id'))

        