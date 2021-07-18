from django import forms
from service.models import ServicePost, BasicPacket, StandardPacket, PremiumPacket
from blog.models import Category, SubCategory

class CreateServicePostForm(forms.ModelForm):

	class Meta:
		model = ServicePost
		fields = ['title', 'description', 'category','subcategory','image']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['subcategory'].queryset = SubCategory.objects.none()

		if 'category' in self.data:
			try:
				category_id = int(self.data.get('category'))
				self.fields['subcategory'].queryset = SubCategory.objects.filter(category=category_id).order_by('name')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('name')

class BasicPacketForm(forms.ModelForm):

	class Meta:
		model = BasicPacket
		fields = ['basic_name', 'basic_desc', 'basic_delivery', 'basic_revision', 'basic_price']

class StandardPacketForm(forms.ModelForm):

	class Meta:
		model = StandardPacket
		fields = ['standard_name', 'standard_desc', 'standard_delivery', 'standard_revision', 'standard_price']

class PremiumPacketForm(forms.ModelForm):

	class Meta:
		model = PremiumPacket
		fields = ['premium_name', 'premium_desc', 'premium_delivery', 'premium_revision', 'premium_price']

class UpdateServiceForm(forms.ModelForm):

	class Meta:
		model = ServicePost
		fields = ['title', 'description', 'image','category','subcategory']

	def save(self, commit=True):
		service = self.instance
		service.title = self.cleaned_data['title']
		service.description = self.cleaned_data['description']
		service.category = self.cleaned_data['category']
		service.subcategory = self.cleaned_data['subcategory']

		if self.cleaned_data['image']:
			service.image = self.cleaned_data['image']

		if commit:
			service.save()
		return service

class UpdateBasicForm(forms.ModelForm):

	class Meta:
		model = BasicPacket
		fields = ['basic_name', 'basic_desc', 'basic_delivery','basic_revision','basic_price']

	def save(self, commit=True):
		basic = self.instance
		basic.name = self.cleaned_data['basic_name']
		basic.desc = self.cleaned_data['basic_desc']
		basic.delivery = self.cleaned_data['basic_delivery']
		basic.revision = self.cleaned_data['basic_revision']
		basic.price = self.cleaned_data['basic_price']

		if commit:
			basic.save()
		return basic

class UpdateStandardForm(forms.ModelForm):

	class Meta:
		model = StandardPacket
		fields = ['standard_name', 'standard_desc', 'standard_delivery','standard_revision','standard_price']

	def save(self, commit=True):
		standard = self.instance
		standard.name = self.cleaned_data['standard_name']
		standard.desc = self.cleaned_data['standard_desc']
		standard.delivery = self.cleaned_data['standard_delivery']
		standard.revision = self.cleaned_data['standard_revision']
		standard.price = self.cleaned_data['standard_price']

		if commit:
			standard.save()
		return standard

class UpdatePremiumForm(forms.ModelForm):

	class Meta:
		model = PremiumPacket
		fields = ['premium_name', 'premium_desc', 'premium_delivery','premium_revision','premium_price']

	def save(self, commit=True):
		premium = self.instance
		premium.name = self.cleaned_data['premium_name']
		premium.desc = self.cleaned_data['premium_desc']
		premium.delivery = self.cleaned_data['premium_delivery']
		premium.revision = self.cleaned_data['premium_revision']
		premium.price = self.cleaned_data['premium_price']

		if commit:
			premium.save()
		return premium

