from django.db import models

class StoredFile(models.Model):
	uuid = models.CharField(max_length=36)
	extension = models.CharField(max_length=8)
	uploaded = models.DateTimeField(auto_now=True)
	amount = models.FloatField()
	destAddress = models.CharField(max_length=34)
	
	def __unicode__(self):
		return self.uuid

class Request(models.Model):
	storedFile = models.ForeignKey(StoredFile)
	address = models.CharField(max_length=34)
	generated = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.address
