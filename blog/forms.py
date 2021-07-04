from django import forms
from blog.models import BlogPost, Category, SubCategory

class CreateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image','category','subcategory','deadline','budget']

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

class UpdateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image','category','subcategory','deadline','budget']

	def save(self, commit=True):
		blog_post = self.instance
		blog_post.title = self.cleaned_data['title']
		blog_post.body = self.cleaned_data['body']
		blog_post.category = self.cleaned_data['category']
		blog_post.subcategory = self.cleaned_data['subcategory']
		blog_post.deadline = self.cleaned_data['deadline']
		blog_post.budget = self.cleaned_data['budget']

		if self.cleaned_data['image']:
			blog_post.image = self.cleaned_data['image']

		if commit:
			blog_post.save()
		return blog_post