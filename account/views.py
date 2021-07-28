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
	Education,
	Report,
	)

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
	project_working = ProjectList.objects.filter(user=request.user, status='working').all()
	project_rejected = ProjectList.objects.filter(user=request.user, status='rejected').all()
	project_waiting = ProjectList.objects.filter(user=request.user, status='waiting').all()
	project_revision = ProjectList.objects.filter(user=request.user, status='revision').all()
	project_canceled = ProjectList.objects.filter(user=request.user, status='canceled').all()
	project_finished = ProjectList.objects.filter(user=request.user, status='finished').all()
	account = Account.objects.filter(email=request.user.email).first()

	if request.POST.get('report'):
		project_id = request.POST.get('project_id')
		print('ini project id:', project_id)
		text = request.POST.get('report')
		print('ini text:', text)
		project = ProjectList.objects.filter(project=project_id).first()
		print('ini project:', project)
		Report.objects.create(
			report_from = request.user,
			report_text = text,
			project = project
		)
		
		return redirect("projectlist")

	context['project_pending'] = project_pending
	context['project_working'] = project_working
	context['project_rejected'] = project_rejected
	context['project_waiting'] = project_waiting
	context['project_revision'] = project_revision
	context['project_canceled'] = project_canceled
	context['project_finished'] = project_finished
	context['account'] = account
	

	return render(request, 'account/listproject.html', context)

@login_required
def service_view(request):

	context={}

	user = request.user
	service_pending = ServiceList.objects.filter(user=request.user, status='pending').all()
	service_working = ServiceList.objects.filter(user=request.user, status='working').all()
	service_rejected = ServiceList.objects.filter(user=request.user, status='rejected').all()
	service_waiting = ServiceList.objects.filter(user=request.user, status='waiting').all()
	service_revision = ServiceList.objects.filter(user=request.user, status='revision').all()
	service_canceled = ServiceList.objects.filter(user=request.user, status='canceled').all()
	service_finished = ServiceList.objects.filter(user=request.user, status='finished').all()
	account = Account.objects.filter(email=request.user.email).first()

	context['service_pending'] = service_pending
	context['service_working'] = service_working
	context['service_rejected'] = service_rejected
	context['service_waiting'] = service_waiting
	context['service_revision'] = service_revision
	context['service_canceled'] = service_canceled
	context['service_finished'] = service_finished
	context['account'] = account
	

	return render(request, 'account/listservice.html', context)

@login_required
def profile_view(request, slug):
	
	context={}
	user = request.user

	
	account = get_object_or_404(Account, slug=slug)
	project_list = BlogPost.objects.filter(author=account.id).all()
	service_list = ServicePost.objects.filter(author=account.id).all()
	project_count = BlogPost.objects.filter(author=account.id).count()
	service_count = ServicePost.objects.filter(author=account.id).count()
	service_feedback = ServiceList.objects.filter(service__in=service_list, status='finished').all()
	service_feedback_count = ServiceList.objects.filter(service__in=service_list, status='finished').count()
	
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
	context['project_count'] = project_count
	context['service_count'] = service_count
	context['service_feedback'] = service_feedback
	context['service_feedback_count'] = service_feedback_count

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
	account = get_object_or_404(Account, slug=slug)

	projectlist = BlogPost.objects.filter(author=user).all()
	projectreqpending = ProjectList.objects.filter(project__in=projectlist, status='pending').all()
	projectreqworking = ProjectList.objects.filter(project__in=projectlist, status='working').all()
	projectreqwaiting = ProjectList.objects.filter(project__in=projectlist, status='waiting').all()
	projectreqrevision = ProjectList.objects.filter(project__in=projectlist, status='revision').all()
	projectreqcanceled = ProjectList.objects.filter(project__in=projectlist, status='canceled').all()
	projectreqfinished = ProjectList.objects.filter(project__in=projectlist, status='finished').all()

	servicelist = ServicePost.objects.filter(author=user).all()
	servicereqpending = ServiceList.objects.filter(service__in=servicelist, status='pending').all()
	servicereqworking = ServiceList.objects.filter(service__in=servicelist, status='working').all()
	servicereqwaiting = ServiceList.objects.filter(service__in=servicelist, status='waiting').all()
	servicereqrevision = ServiceList.objects.filter(service__in=servicelist, status='revision').all()
	servicereqcanceled = ServiceList.objects.filter(service__in=servicelist, status='canceled').all()
	servicereqfinished = ServiceList.objects.filter(service__in=servicelist, status='finished').all()
	
	if request.POST.get('projectoption'):

		pl_id = request.POST.get('project_id')
		project = ProjectList.objects.filter(pl_id=pl_id).first()

		if (request.POST.get('projectoption') == 'accept'):
			project.status = 'working'
			project.save()
			return redirect("dashboard", slug=user.slug)
		elif (request.POST.get('projectoption') == 'decline'):
			project.status = 'rejected'
			blog_post = project.project
			blog_post.status = 'avail'
			blog_post.save()
			project.save()
			return redirect("dashboard", slug=user.slug)
		elif (request.POST.get('projectoption') == 'cancel'):
			project.status = 'canceled'
			project.save()
			return redirect("dashboard", slug=user.slug)
		elif (request.POST.get('projectoption') == 'revision'):
			project.status = 'revision'
			project.save()
			return redirect("dashboard", slug=user.slug)
		elif (request.POST.get('projectoption') == 'finish'):
			pl_id = request.POST.get('project_id')
			return redirect("feedback", project_id=pl_id)


	if request.POST.get('serviceoption'):

		sl_id = request.POST.get('service_id')
		service = ServiceList.objects.filter(sl_id=sl_id).first()

		if (request.POST.get('serviceoption') == 'accept'):
			service.status = 'working'
			service.save()
			return redirect("dashboard", slug=user.slug)
		elif (request.POST.get('serviceoption') == 'decline'):
			service.status = 'rejected'
			service.save()
			return redirect("dashboard", slug=user.slug)
		elif (request.POST.get('serviceoption') == 'finish'):
			service.status = 'waiting'
			service.save()
			return redirect("dashboard", slug=user.slug)
		elif (request.POST.get('serviceoption') == 'cancel'):
			service.status = 'canceled'
			service.save()
			return redirect("dashboard", slug=user.slug)

	if request.POST.get('report'):
		service_id = request.POST.get('service_id')
		text = request.POST.get('report')
		service = ServiceList.objects.filter(service=service_id).first()
		Report.objects.create(
			report_from = request.user,
			report_text = text,
			service = service
		)

		return redirect("dashboard", slug=user.slug)




	context['user'] = user
	context['account'] = account

	context['projectreqpending'] = projectreqpending
	context['projectreqworking'] = projectreqworking
	context['projectreqwaiting'] = projectreqwaiting
	context['projectreqrevision'] = projectreqrevision
	context['projectreqcanceled'] = projectreqcanceled
	context['projectreqfinished'] = projectreqfinished

	context['servicereqpending'] = servicereqpending
	context['servicereqworking'] = servicereqworking
	context['servicereqwaiting'] = servicereqwaiting
	context['servicereqrevision'] = servicereqrevision
	context['servicereqcanceled'] = servicereqcanceled
	context['servicereqfinished'] = servicereqfinished

	return render(request, 'account/dashboard.html', context)

@login_required
def feedback_view(request, project_id):
	
	context={}

	user = request.user
	account = get_object_or_404(Account, slug=user.slug)

	projectlist = BlogPost.objects.filter(author=user).all()
	projectreqpending = ProjectList.objects.filter(project__in=projectlist, status='pending')
	projectreqworking = ProjectList.objects.filter(project__in=projectlist, status='working')
	projectreqdone = ProjectList.objects.filter(project__in=projectlist, status='done')

	servicelist = ServicePost.objects.filter(author=user).all()
	servicereqpending = ServiceList.objects.filter(service__in=servicelist, status='pending')
	servicereqworking = ServiceList.objects.filter(service__in=servicelist, status='working')
	servicereqdone = ServiceList.objects.filter(service__in=servicelist, status='done')
	
	if request.POST.get('rate') and request.POST.get('feedback') :
		project_req = ProjectList.objects.filter(pl_id=project_id).first()
		rating = request.POST.get('rate')
		feedback = request.POST.get('feedback')
		project_req.rating = rating
		project_req.feedback = feedback
		project_req.status = 'finished'
		user = project_req.user
		user.wallet += project_req.project.budget
		user.save()
		project_req.save()
		return redirect("dashboard", slug=request.user.slug)


	context['user'] = user
	context['account'] = account
	context['projectreqpending'] = projectreqpending
	context['projectreqworking'] = projectreqworking
	context['projectreqdone'] = projectreqdone
	context['servicereqpending'] = servicereqpending
	context['servicereqworking'] = servicereqworking
	context['servicereqdone'] = servicereqdone

	return render(request, 'account/feedback-rating.html', context)

@login_required
def feedback_service_view(request, service_id):
	
	context={}

	user = request.user
	service_pending = ServiceList.objects.filter(user=request.user, status='pending').all()
	service_working = ServiceList.objects.filter(user=request.user, status='working').all()
	service_rejected = ServiceList.objects.filter(user=request.user, status='rejected').all()
	service_waiting = ServiceList.objects.filter(user=request.user, status='waiting').all()
	service_revision = ServiceList.objects.filter(user=request.user, status='revision').all()
	service_canceled = ServiceList.objects.filter(user=request.user, status='canceled').all()
	service_finished = ServiceList.objects.filter(user=request.user, status='finished').all()
	account = Account.objects.filter(email=request.user.email).first()

	if request.POST.get('rate') and request.POST.get('feedback') :
		service_req = ServiceList.objects.filter(service=service_id).first()
		rating = request.POST.get('rate')
		feedback = request.POST.get('feedback')
		service_req.rating = rating
		service_req.feedback = feedback
		service_req.status = 'finished'
		service_req.save()
		return redirect("servicelist")

	context['service_pending'] = service_pending
	context['service_working'] = service_working
	context['service_rejected'] = service_rejected
	context['service_waiting'] = service_waiting
	context['service_revision'] = service_revision
	context['service_canceled'] = service_canceled
	context['service_finished'] = service_finished
	context['account'] = account

	return render(request, 'account/feedback-rating-service.html', context)

@login_required
def finish_project(request, project_id):
	
	context={}
	user = request.user

	project = ProjectList.objects.filter(pl_id=project_id).first()

	project.status = 'waiting'
	project.save()

	return redirect('projectlist')

@login_required
def cancel_project(request, project_id):
	
	context={}
	user = request.user

	project = ProjectList.objects.filter(pl_id=project_id).first()

	project.status = 'canceled'
	project.save()

	return redirect('projectlist')

@login_required
def finish_service(request, service_id):
	
	context={}
	user = request.user

	service = ServiceList.objects.filter(sl_id=service_id).first()

	service.status = 'finished'
	service.save()

	return redirect('servicelist')

@login_required
def cancel_service(request, service_id):
	
	context={}
	user = request.user

	service = ServiceList.objects.filter(sl_id=service_id).first()

	service.status = 'canceled'
	service.save()

	return redirect('servicelist')

@login_required
def revision_service(request, service_id):
	
	context={}
	user = request.user

	service = ServiceList.objects.filter(sl_id=service_id).first()

	service.status = 'revision'
	service.save()

	return redirect('servicelist')