from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

def upload_location(instance, filename):
	file_path = 'blog/{author_id}/{title}-{filename}'.format(
				author_id=str(instance.author.id),title=str(instance.title), filename=filename)
	return file_path


class Category(models.Model):
    name 					= models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category 				= models.ForeignKey(Category, on_delete=models.CASCADE)
    name 					= models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
	post_id					= models.IntegerField(primary_key=True)
	title 					= models.CharField(max_length=50, null=False, blank=False)
	body 					= models.TextField(max_length=2000, null=False, blank=False)
	image		 			= models.ImageField(upload_to=upload_location, null=True, blank=True)
	date_published 			= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated 			= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	category 				= models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
	subcategory 			= models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=False)
	deadline 				= models.PositiveIntegerField(blank=False, null=False)
	budget 					= models.BigIntegerField(blank=False, null=False)
	status					= models.CharField(max_length=50, null=False, blank=False, default='avail')
	slug 					= models.SlugField()

	def __str__(self):
		return self.title

	def add_to_projectlist(self):
		return reverse("blog:add-to-projectlist", kwargs={
			'slug': self.slug
		})



@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 

def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)