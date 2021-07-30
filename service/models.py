from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

def upload_location(instance, filename):
	file_path = 'service/{author_id}/{title}-{filename}'.format(
				author_id=str(instance.author.id),title=str(instance.title), filename=filename)
	return file_path

class ServicePost(models.Model):
	title 					= models.CharField(max_length=50, null=False, blank=False)
	description				= models.TextField(max_length=2000, null=False, blank=False)
	date_published 			= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated 			= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	category				= models.ForeignKey(settings.AUTH_CAT_MODEL, on_delete=models.CASCADE, null=True, blank=True)
	subcategory				= models.ForeignKey(settings.AUTH_SUBCAT_MODEL, on_delete=models.CASCADE, null=True, blank=True)
	image		 			= models.ImageField(upload_to=upload_location, null=True, blank=True)
	slug 					= models.SlugField()

	def __str__(self):
		return self.title

	def add_to_servicelist(self):
		return reverse("service:add-to-servicelist", kwargs={
			'slug': self.slug
		})

class BasicPacket(models.Model):
    basic_id                = models.IntegerField(primary_key=True)
    basic_name 				= models.CharField(max_length=100, null=True, blank=True)
    basic_desc 				= models.CharField(max_length=100, null=True, blank=True)
    basic_delivery 			= models.PositiveIntegerField(blank=True, null=True)
    basic_revision 			= models.PositiveIntegerField(blank=True, null=True)
    basic_price 			= models.BigIntegerField(blank=False, null=True)
    packet_service			= models.ForeignKey(ServicePost, on_delete=models.CASCADE, null=True, blank=True)
    tipe_packet             = models.CharField(max_length=20,default='basic')

    def __str__(self):
        return self.basic_name

class StandardPacket(models.Model):
    standard_id             = models.IntegerField(primary_key=True)
    standard_name 			= models.CharField(max_length=100, null=True, blank=True)
    standard_desc 			= models.CharField(max_length=100, null=True, blank=True)
    standard_delivery 		= models.PositiveIntegerField(blank=True, null=True)
    standard_revision 		= models.PositiveIntegerField(blank=True, null=True)
    standard_price 			= models.BigIntegerField(blank=False, null=True)
    packet_service			= models.ForeignKey(ServicePost, on_delete=models.CASCADE, null=True, blank=True)
    tipe_packet             = models.CharField(max_length=20,default='standard')

    def __str__(self):
        return self.standard_name

class PremiumPacket(models.Model):
    premium_id              = models.IntegerField(primary_key=True)
    premium_name 			= models.CharField(max_length=100, null=True, blank=True)
    premium_desc 			= models.CharField(max_length=100, null=True, blank=True)
    premium_delivery 		= models.PositiveIntegerField(blank=True, null=True)
    premium_revision 		= models.PositiveIntegerField(blank=True, null=True)
    premium_price 			= models.BigIntegerField(blank=False, null=True)
    packet_service			= models.ForeignKey(ServicePost, on_delete=models.CASCADE, null=True, blank=True)
    tipe_packet             = models.CharField(max_length=20,default='premium')

    def __str__(self):
        return self.premium_name


@receiver(post_delete, sender=ServicePost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 

def pre_save_service_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_service_post_receiver, sender=ServicePost)