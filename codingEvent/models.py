from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.URLField(max_length = 200)
    video = models.URLField(max_length = 200)
    category = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    active = models.BooleanField()
    startingAt = models.CharField(max_length=50)
    postingAt = models.DateTimeField(auto_now_add=True)
    seatTaken = models.IntegerField()

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, blank=True)
    postingAt = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class Interest(models.Model):
    owner =  models.ForeignKey(User, on_delete=models.CASCADE)
    event =  models.ForeignKey(Event, on_delete=models.CASCADE)
    going = models.BooleanField()
    planing = models.BooleanField()
    planingImportant = models.BooleanField()
    


    
