from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

# Create your models here.

def upload_location(instance, filename):
	file_path = 'organization/{author_id}/{title}-{filename}'.format(
				author_id=str(instance.author.id),title=str(instance.name), filename=filename)
	return file_path

class Organization(models.Model):
	name					= models.CharField(max_length=50, null=False, blank=False, unique=True)
	description				= models.TextField(max_length=1000, null=False, blank=False)
	def __str__(self):
		return self.name

class Member(models.Model):
	organization			= models.ForeignKey(Organization, related_name="members", on_delete=models.CASCADE)
	user					= models.CharField(max_length=50)
	def __str__(self):
		return '%s - %s' %(self.organization, self.user)