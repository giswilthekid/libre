from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from blog.models import BlogPost, Category, SubCategory
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account, ProjectList
from service.models import ServicePost

@login_required
def buyerpage(request):

	context = {}
	user = request.user
	account = Account.objects.filter(email=request.user.email).first()
	blog_posts = BlogPost.objects.filter(status='avail').all()

	if request.POST.get('topup'):
		topup = request.POST.get('topup')
		user.wallet += int(topup)
		user.save()
		return redirect('buyerpage')


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
		budget = request.POST.get('budget')
		if user.wallet < int(budget):
			print('uang kurang, silakan top up duls')
			return redirect('buyerpage')
		else:
			author = Account.objects.filter(email=request.user.email).first()
			user.wallet -= int(budget)
			obj.author = author
			obj.save()
			user.save()
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
	avail_post = BlogPost.objects.filter(slug=slug).first()
	applied_post= BlogPost.objects.filter(slug=slug, status='applied')
	project_count = BlogPost.objects.filter(author=avail_post.author).count()
	service_count = ServicePost.objects.filter(author=avail_post.author).count()


	context['avail_post'] = avail_post
	context['account'] = account
	context['applied_post'] = applied_post
	context['project_count'] = project_count
	context['service_count'] = service_count


	return render(request, 'blog/post_detail.html', context)

def add_to_projectlist(request, slug):

	project = get_object_or_404(BlogPost, slug=slug)

	order_project = ProjectList.objects.filter(project=project, user=request.user)
	order_project = ProjectList.objects.create(
	project=project,
	user=request.user,
	status='pending'
	)
	project.status = 'applied'
	project.save()
	print(project.slug)
	return redirect("projectlist")

	return redirect('buyerpage')

def cancelled_project(request, slug):

	project = get_object_or_404(BlogPost, slug=slug)
	order_project = ProjectList.objects.filter(project=project, user=request.user)
	project.status = 'avail'
	project.save()
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
	author = request.user
	author.wallet += blog_post.budget
	author.save()
	blog_post.delete()

	return redirect("buyerpage")


