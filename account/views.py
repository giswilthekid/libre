from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


from account.forms import RegistrationForm, AccountAuthenticationForm
from account.models import Account, ProjectList

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
	project = ProjectList.objects.filter(user=request.user).all()
	account = Account.objects.filter(email=request.user.email).first()

	context['project'] = project
	context['account'] = account

	return render(request, 'account/listproject.html', context)

@login_required
def profile_view(request):
	
	context={}

	account = Account.objects.filter(email=request.user.email).first()
	context['account'] = account

	return render(request, 'account/profile.html', context)
