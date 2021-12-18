from django.db import models
from datetime import datetime

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
    pass_room = models.CharField(max_length=1000, default=None)

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)

class Customer(models.Model):
    username = models.CharField(max_length=1000000)
    password = models.CharField(max_length=1000000)