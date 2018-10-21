from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    location = models.CharField(max_length=120)
    datetime = models.DateTimeField()
    seats = models.IntegerField()
    organizer = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

