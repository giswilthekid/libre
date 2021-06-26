from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.utils.text import slugify

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
	first_name				= models.CharField(max_length=50)
	last_name				= models.CharField(max_length=50)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

class ProjectList(models.Model):
	status					= models.CharField(max_length=20, default='pending')
	project					= models.ForeignKey(settings.AUTH_BLOG_MODEL, on_delete=models.CASCADE)
	user 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	timestamp	 			= models.DateTimeField(auto_now_add=True, verbose_name="timestamp")

	def __str__(self):
		return self.status