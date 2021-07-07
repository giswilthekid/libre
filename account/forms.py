from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account, ProjectList, Language, Skill, Education

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

	class Meta:
		model = Account 
		fields = ('email', 'username', 'password1', 'password2','image', 'first_name', 'last_name')

class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")


class UpdateProfileForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ['first_name', 'last_name', 'origin','image', 'status', 'description']

	def save(self, commit=True):
		account = self.instance
		account.first_name = self.cleaned_data['first_name']
		account.last_name = self.cleaned_data['last_name']
		account.origin = self.cleaned_data['origin']
		account.status = self.cleaned_data['status']
		account.description = self.cleaned_data['description']

		if self.cleaned_data['image']:
			account.image = self.cleaned_data['image']

		if commit:
			account.save()
		return account

class UpdateLanguageForm(forms.ModelForm):

	class Meta:
		model = Language
		fields = ['language_name', 'language_level']

	def save(self, commit=True):
		language = self.instance
		language.language_name = self.cleaned_data['language_name']
		language.language_level = self.cleaned_data['language_level']

		if commit:
			language.save()
		return language

class UpdateSkillForm(forms.ModelForm):

	class Meta:
		model = Skill
		fields = ['skill_name', 'skill_level']

	def save(self, commit=True):
		skill = self.instance
		skill.skill_name = self.cleaned_data['skill_name']
		skill.skill_level = self.cleaned_data['skill_level']

		if commit:
			skill.save()
		return skill

class UpdateEducationForm(forms.ModelForm):

	class Meta:
		model = Education
		fields = ['country', 'collage','title','major','year']

	def save(self, commit=True):
		education = self.instance
		education.country = self.cleaned_data['country']
		education.collage = self.cleaned_data['collage']
		education.title = self.cleaned_data['title']
		education.major = self.cleaned_data['major']
		education.year = self.cleaned_data['year']

		if commit:
			education.save()
		return education

