from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from multi_email_field.fields import MultiEmailField
import os


class Class(models.Model):
	slug = models.SlugField(max_length=50, null=True, unique=True)
	user = models.ManyToManyField(User, related_name='myclass')
	subject = models.CharField(max_length=100, null=True)
	description = models.TextField(max_length=250, null=True, blank=True)


	def __str__(self):
		return self.slug

class Priority(models.Model):
	myclass = models.ForeignKey(Class, related_name='priority', on_delete=models.CASCADE)
	to = MultiEmailField()
	expiry_date = models.DateField()
	expiry_time = models.TimeField()
	mylist = models.TextField(blank=True, null=True)

	def set_list(self, element):
		if self.mylist:
			self.mylist =  self.mylist + element + ","
		else:
			self.mylist =  element + ","

	def remove_list(self, element):
		if self.mylist:
			mylist = self.mylist.split(",")
			if element in mylist:
				element_raplace = element + ','
				self.mylist = self.mylist.replace(element_raplace, '')
				print(self.mylist)
				
	def get_list(self):
		if self.mylist:
			return self.mylist.split(",")[:-1]
		else:
			return []

	def len_list(self):
		if self.mylist:
			return len(self.mylist.split(","))-1
		else:
			return 0

class ClassGroup(models.Model):
	myclass = models.ForeignKey(Class, related_name='class_group', on_delete=models.CASCADE)
	max_size = models.IntegerField(null=True)
	expiry_date = models.DateField(null=True)
	expiry_time = models.TimeField(null=True)
	mylist = models.TextField(blank=True, null=True)

	def set_list(self, element):
		if self.mylist:
			self.mylist =  self.mylist + element + ","
		else:
			self.mylist =  element + ","

	def remove_list(self, element):
		if self.mylist:
			mylist = self.mylist.split(",")
			if element in mylist:
				element_raplace = element + ','
				self.mylist = self.mylist.replace(element_raplace, '')
				print(self.mylist)

	def get_list(self):
		if self.mylist:
			return self.mylist.split(",")[:-1]
		else:
			return []

	def len_list(self):
		if self.mylist:
			return len(self.mylist.split(","))-1
		else:
			return 0


	