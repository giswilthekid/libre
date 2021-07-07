from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from blog.models import BlogPost, Category, SubCategory
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account, ProjectList

@login_required
def buyerpage(request):

	context = {}
	user = request.user
	account = Account.objects.filter(email=request.user.email).first()

	blog_posts = BlogPost.objects.all()
	context['blog_posts'] = blog_posts
	context['account'] = account

	return render(request, 'blog/buyerpage.html', context)

@login_required
def create_post_view(request):

	context = {}

	user = request.user

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=request.user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()

		return redirect('buyerpage')

	category = Category.objects.all()
	account = Account.objects.filter(email=request.user.email).first()

	context['form'] = form
	context['account'] = account
	context['category'] = category


	return render(request, 'blog/create_post.html', context)

def load_subcategory(request):
	category_id = request.GET.get('category')
	subcategory = SubCategory.objects.filter(category=category_id).order_by('name')
	return render(request, 'blog/subcategory_dropdown_list_options.html', {'subcategory': subcategory})

@login_required
def detail_blog_view(request, slug):
	
	context = {}

	account = Account.objects.filter(email=request.user.email).first()
	blog_post = get_object_or_404(BlogPost, slug=slug)
	order_project = ProjectList.objects.filter(project=blog_post, user=request.user)
	project_count = BlogPost.objects.filter(author=blog_post.author).count()

	context['blog_post'] = blog_post
	context['account'] = account
	context['order_project'] = order_project
	context['project_count'] = project_count


	return render(request, 'blog/post_detail.html', context)

def add_to_projectlist(request, slug):

	project = get_object_or_404(BlogPost, slug=slug)

	order_project = ProjectList.objects.filter(project=project, user=request.user)
	if order_project.exists():
		print('Project Sudah Ada')
	else:
		order_project = ProjectList.objects.create(
		project=project,
		user=request.user,
		status='pending'
		)
		print(project.slug)
		return redirect("projectlist")

	return redirect('buyerpage')

def cancelled_project(request, slug):

	project = get_object_or_404(BlogPost, slug=slug)
	order_project = ProjectList.objects.filter(project=project, user=request.user)

	order_project.delete()

	return redirect('projectlist')

def edit_post_view(request, slug):
	
	context = {}
	user = request.user

	account = Account.objects.filter(email=request.user.email).first()
	

	blog_post = get_object_or_404(BlogPost, slug=slug)
	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			blog_post = obj

			return redirect('buyerpage')

	category = Category.objects.all()
	
	form = UpdateBlogPostForm(
			initial={
					"title": blog_post.title, 
					"body": blog_post.body,
					"image": blog_post.image,
					"category": blog_post.category,
					"subcategory": blog_post.subcategory,
					"deadline": blog_post.deadline,
					"budget": blog_post.budget,
				}
			)

	context['form'] = form
	context['account'] = account
	context['category'] = category
	context['blog_post'] = blog_post

	return render(request, 'blog/edit_post.html', context)

def delete_post_view(request, slug):
	
	context = {}
	blog_post = get_object_or_404(BlogPost, slug=slug)
	blog_post.delete()

	return redirect("buyerpage")


