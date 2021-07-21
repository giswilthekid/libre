from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


from account.forms import(
	RegistrationForm, 
	AccountAuthenticationForm, 
	UpdateProfileForm, 
	UpdateLanguageForm, 
	UpdateSkillForm, 
	UpdateEducationForm,
	)

from account.models import(
	Account, 
	ProjectList,
	ServiceList,
	Language, 
	Skill, 
	Education,)

from blog.models import BlogPost
from service.models import ServicePost, BasicPacket, StandardPacket, PremiumPacket

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
def service_view(request):

	context={}

	user = request.user
	service_pending = ServiceList.objects.filter(user=request.user, status='pending').all()
	service_ongoing = ServiceList.objects.filter(user=request.user, status='ongoing').all()
	service_done = ServiceList.objects.filter(user=request.user, status='done').all()
	service_declined = ServiceList.objects.filter(user=request.user, status='cancelled').all()
	account = Account.objects.filter(email=request.user.email).first()

	context['service_pending'] = service_pending
	context['service_ongoing'] = service_ongoing
	context['service_done'] = service_done
	context['service_declined'] = service_declined
	context['account'] = account
	

	return render(request, 'account/listservice.html', context)

@login_required
def profile_view(request, slug):
	
	context={}
	user = request.user

	
	account = get_object_or_404(Account, slug=slug)
	project_list = BlogPost.objects.filter(author=account.id).all()
	
	if request.POST.get('status'):
		account.status = request.POST.get('status')
		account.save()
		return redirect('profile', slug=slug)

	if request.POST.get('description'):
		account.description = request.POST.get('description')
		account.save()
		return redirect('profile', slug=slug)

	formlanguage = UpdateLanguageForm(request.POST or None)
	if formlanguage.is_valid() and request.POST.get('language_name') and request.POST.get('language_level') :
		obj = formlanguage.save(commit=False)
		author = Account.objects.filter(email=request.user.email).first()
		obj.author = author
		obj.save()
		formlanguage = UpdateLanguageForm()
		return redirect('profile', slug=slug)

	formskill = UpdateSkillForm(request.POST or None)
	if formskill.is_valid() and request.POST.get('skill_name') and request.POST.get('skill_level'):
		obj = formskill.save(commit=False)
		author = Account.objects.filter(email=request.user.email).first()
		obj.author = author
		obj.save()
		formskill = UpdateSkillForm()
		return redirect('profile', slug=slug)

	formsedu = UpdateEducationForm(request.POST or None)
	if formsedu.is_valid() and request.POST.get('country') and request.POST.get('collage') and request.POST.get('title') and request.POST.get('major') and request.POST.get('year'):
		obj = formsedu.save(commit=False)
		author = Account.objects.filter(email=request.user.email).first()
		obj.author = author
		obj.save()
		formsedu = UpdateEducationForm()
		return redirect('profile', slug=slug)

	language = Language.objects.filter(author=account.id)
	skill = Skill.objects.filter(author=account.id)
	education = Education.objects.filter(author=account.id)
	
	form = UpdateProfileForm(
			initial={
					"first_name": account.first_name, 
					"last_name": account.last_name,
					"origin": account.origin,
					"image": account.image,
					"status": account.status,
					"description": account.description,
				}
			)

	context['user'] = user
	context['form'] = form
	context['account'] = account
	context['project_list'] = project_list
	context['language'] = language
	context['skill'] = skill
	context['education'] = education

	return render(request, 'account/profile.html', context)

@login_required
def delete_language(request, id):
	
	language = get_object_or_404(Language, id=id)
	language.delete()

	user = request.user
	slug = user.slug

	return redirect("profile", slug=slug)

@login_required
def delete_skill(request, id):
	
	skill = get_object_or_404(Skill, id=id)
	skill.delete()

	user = request.user
	slug = user.slug

	return redirect("profile", slug=slug)

@login_required
def delete_education(request, id):
	
	education = get_object_or_404(Education, id=id)
	education.delete()

	user = request.user
	slug = user.slug

	return redirect("profile", slug=slug)

@login_required
def dashboard_view(request, slug):
	
	context={}

	user = request.user

	project = BlogPost.objects.filter(author=user).all()
	projectreqpending = ProjectList.objects.filter(project__in=project, status='pending')
	projectreqongoing = ProjectList.objects.filter(project__in=project, status='ongoing')

	service = ServicePost.objects.filter(author=user).all()
	servicereq = ServiceList.objects.filter(service__in=service)

	
	account = get_object_or_404(Account, slug=slug)

	pl_id = request.POST.get('project_id')
	project = ProjectList.objects.filter(pl_id=pl_id).first()
	user = request.user
	print(project)
	
	if (request.POST.get('statusoption') == 'accept'):
		project.status = 'ongoing'
		project.save()
		return redirect("dashboard", slug=user.slug)
	elif (request.POST.get('statusoption') == 'decline'):
		project.status = 'cancelled'
		project.save()
		return redirect("dashboard", slug=user.slug)
	else:
		print('nothing')


	context['user'] = user
	context['account'] = account
	context['projectreqpending'] = projectreqpending
	context['projectreqongoing'] = projectreqongoing
	context['servicereq'] = servicereq

	return render(request, 'account/dashboard.html', context)

@login_required
def status_change(request):

	project_id = request.POST.get('project_id')
	project = ProjectList.objects.filter(id=project_id)
	user = request.user
	print(project_id)
	
	if request.POST:
		if (request.POST.get('statusoption') == 'accept'):
			project.status = 'ongoing'
			return redirect("buyerpage")
		elif (request.POST.get('statusoption') == 'decline'):
			project.status = 'cancelled'
			return redirect("buyerpage")
		else:
			print('nothing')