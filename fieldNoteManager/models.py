from django.db import models

# Create your models here.
class User(models.Model):
    userName = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
class Excursion(models.Model):
    user = models.ForeignKey(User)
    location = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
       
class Sighting(models.Model):
    excursion = models.ForeignKey(Excursion)
    species = models.CharField(max_length=100)
    

        