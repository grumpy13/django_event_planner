from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)
	location = models.CharField(max_length=30, blank=True)
	birth_date = models.DateField(null=True, blank=True)

	def get_full_name(self):
		full_name = '%s %s' % (self.user.first_name, self.user.last_name)
		return full_name.strip()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


