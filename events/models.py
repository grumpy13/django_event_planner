from django.db import models
from django.contrib.auth.models import User
import datetime

class Event(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    location = models.CharField(max_length=120)
    date = models.DateField()
    time = models.TimeField()
    seats = models.IntegerField()
    organizer = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_remaining_seats(self):
    	num_of_tickets = sum([b.tickets for b in self.booking_set.all()])
    	return self.seats - num_of_tickets

class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tickets = models.IntegerField()



