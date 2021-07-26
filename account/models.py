from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

def upload_location(instance, filename):
	file_path = 'account/profilepict/{filename}'.format(filename=filename)
	return file_path

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError("Users must have an email address")
		if not username:
			raise ValueError("Users must have an username")

		user = self.model(
			email=self.normalize_email(email),
			username=username,
			)

		user.set_password(password)
		user.save(using=self.db)
		return user

	def create_superuser(self,email,username,password):
		user = self.create_user(
			email=self.normalize_email(email),
			username=username,
			password=password,
			)

		user.is_admin=True
		user.is_staff=True
		user.is_superuser=True
		user.save(using=self.db)
		return user


class Account (AbstractBaseUser):
	email					= models.EmailField(verbose_name='email', unique= True)
	username				= models.CharField(max_length=30, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	image					= models.ImageField(upload_to=upload_location, null=True, blank=True)
	first_name				= models.CharField(max_length=50, null=True, blank=True)
	last_name				= models.CharField(max_length=50, null=True, blank=True)
	origin					= models.CharField(max_length=50, null=True, blank=True)
	status					= models.CharField(max_length=50, null=True, blank=True)
	description				= models.TextField(max_length=2000, null=True, blank=True)
	slug 					= models.SlugField()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

	def get_absolute_url(self):
		return reverse("profile", kwargs={
			'slug': self.slug
	})

@receiver(post_delete, sender=Account)
def pre_save_account_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.username)

pre_save.connect(pre_save_account_receiver, sender=Account)

class ProjectList(models.Model):
	pl_id					= models.IntegerField(primary_key=True)
	status					= models.CharField(max_length=20, default='pending')
	project					= models.ForeignKey(settings.AUTH_BLOG_MODEL, on_delete=models.CASCADE)
	user 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	rating 					= models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], null=True)
	feedback				= models.CharField(max_length=2000, null=True)
	timestamp	 			= models.DateTimeField(auto_now_add=True, verbose_name="timestamp")

	def __str__(self):
		return self.project.title

class ServiceList(models.Model):
	sl_id					= models.IntegerField(primary_key=True)
	status					= models.CharField(max_length=20, default='pending')
	service					= models.ForeignKey(settings.AUTH_SERVICE_MODEL, on_delete=models.CASCADE)
	user 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	basic_packet			= models.ForeignKey(settings.AUTH_BASIC_MODEL, on_delete=models.CASCADE, blank=True, null=True)
	standard_packet			= models.ForeignKey(settings.AUTH_STANDARD_MODEL, on_delete=models.CASCADE, blank=True, null=True)
	premium_packet			= models.ForeignKey(settings.AUTH_PREMIUM_MODEL, on_delete=models.CASCADE, blank=True, null=True)
	rating 					= models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)], null=True)
	feedback				= models.CharField(max_length=2000, null=True)
	timestamp	 			= models.DateTimeField(auto_now_add=True, verbose_name="timestamp")

	def __str__(self):
		return self.service.title

class Language(models.Model):
    language_name 			= models.CharField(max_length=100, null=True, blank=True)
    language_level 			= models.CharField(max_length=100, null=True, blank=True)
    author 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.language_name

class Skill(models.Model):
    skill_name 				= models.CharField(max_length=100, null=False, blank=True)
    skill_level 			= models.CharField(max_length=100, null=False, blank=True)
    author 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.skill_name

class Education(models.Model):
    country 				= models.CharField(max_length=100, null=True, blank=True)
    collage 				= models.CharField(max_length=100, null=True, blank=True)
    title 					= models.CharField(max_length=100, null=True, blank=True)
    major 					= models.CharField(max_length=100, null=True, blank=True)
    year 					= models.CharField(max_length=100, null=True, blank=True)
    author 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.collage