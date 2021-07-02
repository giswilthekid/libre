from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


from account.forms import RegistrationForm, AccountAuthenticationForm
from account.models import Account, ProjectList
from blog.models import BlogPost

def landing_view(request):
	context = {}
	if request.GET:
		context['registration_form'] = RegistrationForm()
		context['login_form'] = AccountAuthenticationForm()
	return render(request, 'account/landingpage.html', context)

def registration_view(request):
	if request.POST:
		form = RegistrationForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('landing')
			messages.success(request, f'Your account has been created! You are now able to log in')
		else:
			form = RegistrationForm()
	return redirect('landing')

def logout_view(request):
	logout(request)
	return redirect('landing')

def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("buyerpage")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("buyerpage")

	return redirect('landing')

@login_required
def project_view(request):

	context={}

	user = request.user
	project_pending = ProjectList.objects.filter(user=request.user, status='pending').all()
	project_ongoing = ProjectList.objects.filter(user=request.user, status='ongoing').all()
	project_done = ProjectList.objects.filter(user=request.user, status='done').all()
	project_declined = ProjectList.objects.filter(user=request.user, status='cancelled').all()
	account = Account.objects.filter(email=request.user.email).first()

	context['project_pending'] = project_pending
	context['project_ongoing'] = project_ongoing
	context['project_done'] = project_done
	context['project_declined'] = project_declined
	context['account'] = account
	

	return render(request, 'account/listproject.html', context)

@login_required
def profile_view(request, slug):
	
	context={}
	user = request.user

	
	account = Account.objects.filter(slug=slug).first()
	project_list = BlogPost.objects.filter(author=account.id).all()

	context['account'] = account
	context['project_list'] = project_list

	return render(request, 'account/profile.html', context)
