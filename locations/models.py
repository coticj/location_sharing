from django.db import models

class Location(models.Model):
	user_ip = models.CharField(max_length=200)
	location = models.CharField(max_length=200)
	lat = models.CharField(max_length=200)
	lon = models.CharField(max_length=200)
	visit_date = models.DateTimeField('date visited')

class User(models.Model):
	user_ip = models.CharField(max_length=200)
	email = models.CharField(max_length=200)