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
