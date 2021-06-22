from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from blog.models import BlogPost
from blog.forms import CreateBlogPostForm
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

	context['form'] = form

	return render(request, 'blog/create_post.html', context)

@login_required
def detail_blog_view(request, slug):
	
	context = {}
	user = request.user
	account = Account.objects.filter(email=request.user.email).first()

	blog_post = get_object_or_404(BlogPost, slug=slug)
	context['blog_post'] = blog_post
	context['account'] = account

	return render(request, 'blog/post_detail.html', context)

def add_to_projectlist(request, slug):

	project = get_object_or_404(BlogPost, slug=slug)

	order_project, created = ProjectList.objects.get_or_create(
		project=project,
		user=request.user,
		status='pending'
	)

	order_project.save()

	print(order_project)
	print('alfianasu')

	return redirect('projectlist')



