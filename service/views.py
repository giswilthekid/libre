from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

from service.models import ServicePost, BasicPacket, StandardPacket, PremiumPacket
from blog.models import Category, SubCategory, BlogPost
from account.models import Account, ProjectList, ServiceList

from service.forms import(
	CreateServicePostForm, 
	BasicPacketForm, 
	StandardPacketForm, 
	PremiumPacketForm,
	UpdateServiceForm,
	UpdateBasicForm,
	UpdateStandardForm,
	UpdatePremiumForm,
	) 

@login_required
def sellerpage(request):

	context = {}
	user = request.user
	account = Account.objects.filter(email=request.user.email).first()
	service = ServicePost.objects.all()

	if request.POST.get('topup'):
		topup = request.POST.get('topup')
		user.wallet += int(topup)
		user.save()
		return redirect('service:sellerpage')

	context['account'] = account
	context['service'] = service

	return render(request, 'service/sellerpage.html', context)

@login_required
def create_service_view(request):

	context = {}

	user = request.user

	form = CreateServicePostForm(request.POST or None, request.FILES or None)
	basicform = BasicPacketForm(request.POST or None)
	standardform = StandardPacketForm(request.POST or None)
	premiumform = PremiumPacketForm(request.POST or None)

	if form.is_valid() and basicform.is_valid() and standardform.is_valid() and premiumform.is_valid() :
		obj = form.save(commit=False)
		author = Account.objects.filter(email=request.user.email).first()
		obj.author = author
		obj.save()
		form = CreateServicePostForm()

		service_packet = ServicePost.objects.filter(id=obj.id).first()

		print(service_packet)

		basic_form = basicform.save(commit=False)
		basic_form.packet_service = service_packet
		basic_form.save()
		basicform = BasicPacketForm()

		standard_form = standardform.save(commit=False)
		standard_form.packet_service = service_packet
		standard_form.save()
		standardform = StandardPacketForm()

		premium_form = premiumform.save(commit=False)
		premium_form.packet_service = service_packet
		premium_form.save()
		premiumform = PremiumPacketForm()

		return redirect('service:sellerpage')
	else:
		print('errors')

	category = Category.objects.all()
	account = Account.objects.filter(email=request.user.email).first()

	context['account'] = account
	context['category'] = category


	return render(request, 'service/create_service.html', context)

@login_required
def detail_service_view(request, slug):
	
	context = {}

	user = request.user
	account = Account.objects.filter(email=request.user.email).first()
	service = get_object_or_404(ServicePost, slug=slug)
	order_service = ServiceList.objects.filter(service=service, user=request.user)
	service_count = ServicePost.objects.filter(author=service.author).count()
	project_count = BlogPost.objects.filter(author=service.author).count()
	basic = get_object_or_404(BasicPacket, packet_service=service)
	standard = get_object_or_404(StandardPacket, packet_service=service)
	premium = get_object_or_404(PremiumPacket, packet_service=service)
	order_queue = ServiceList.objects.filter(service=service, status='pending').count()

	if request.POST.get('topup'):
		topup = request.POST.get('topup')
		user.wallet += int(topup)
		user.save()
		return redirect('service:detail-service', slug=slug)

	context['service'] = service
	context['account'] = account
	context['order_service'] = order_service
	context['service_count'] = service_count
	context['project_count'] = project_count
	context['basic'] = basic
	context['standard'] = standard
	context['premium'] = premium
	context['order_queue'] = order_queue


	return render(request, 'service/service_detail.html', context)

def add_to_servicelist(request, slug, packet_id, tipe_packet):

	service = get_object_or_404(ServicePost, slug=slug)

	if tipe_packet == 'basic':
		basic_packet = BasicPacket.objects.filter(basic_id=packet_id)
		order_service = ServiceList.objects.filter(service=service, user=request.user, basic_packet=basic_packet[0])

		user = request.user
		basicprice = basic_packet[0].basic_price
		if (user.wallet < int(basicprice)):
			print('uang tidak cukup')
		else:
			print('basic:' ,basic_packet)
			order_service = ServiceList.objects.create(
				service=service,
				user=request.user,
				status='pending',
				basic_packet=basic_packet[0]
			)
			user.wallet -= int(basicprice)
			user.save()
			return redirect("servicelist")

	if tipe_packet == 'standard':
		standard_packet = StandardPacket.objects.filter(standard_id=packet_id)
		order_service = ServiceList.objects.filter(service=service, user=request.user, standard_packet=standard_packet[0])

		user = request.user
		standardprice = standard_packet[0].standard_price
		if (user.wallet < int(standardprice)):
			print('uang tidak cukup')
		else:
			order_service = ServiceList.objects.create(
				service=service,
				user=request.user,
				status='pending',
				standard_packet=standard_packet[0]
			)
			user.wallet -= int(standardprice)
			user.save()
			return redirect("servicelist")

	if tipe_packet == 'premium':
		premium_packet = PremiumPacket.objects.filter(premium_id=packet_id)
		order_service = ServiceList.objects.filter(service=service, user=request.user, premium_packet=premium_packet[0])

		user = request.user
		premiumprice = premium_packet[0].premium_price
		if (user.wallet < int(premiumprice)):
			print('uang tidak cukup')
		else:
			order_service = ServiceList.objects.create(
				service=service,
				user=request.user,
				status='pending',
				premium_packet=premium_packet[0]
			)
			user.wallet -= int(premiumprice)
			user.save()
			return redirect("servicelist")

def cancelled_service(request, slug):

	service = get_object_or_404(ServicePost, slug=slug)
	order_service = ServiceList.objects.filter(service=service, user=request.user)

	order_service.delete()

	return redirect('servicelist')

def edit_service_view(request, slug):
	
	context = {}
	user = request.user

	account = Account.objects.filter(email=request.user.email).first()
	

	service = get_object_or_404(ServicePost, slug=slug)
	basic = get_object_or_404(BasicPacket, packet_service=service)
	standard = get_object_or_404(StandardPacket, packet_service=service)
	premium = get_object_or_404(PremiumPacket, packet_service=service)

	if request.POST:

		serviceform = UpdateServiceForm(request.POST or None, request.FILES or None, instance=service)
		basicform = UpdateBasicForm(request.POST or None, instance=basic)
		standardform = UpdateStandardForm(request.POST or None, instance=standard)
		premiumform = UpdatePremiumForm(request.POST or None, instance=premium)

		if serviceform.is_valid() and basicform.is_valid() and standardform.is_valid() and premiumform.is_valid() :
			obj = serviceform.save(commit=False)
			obj.save()
			service = obj

			basicobj = basicform.save(commit=False)
			basicobj.save()
			basic = basicobj

			standardobj = standardform.save(commit=False)
			standardobj.save()
			standard = standardobj

			premiumobj = premiumform.save(commit=False)
			premiumobj.save()
			premium = premiumobj

			return redirect('service:sellerpage')

	category = Category.objects.all()
	
	formservice = UpdateServiceForm(
			initial={
					"title": service.title, 
					"description": service.description,
					"image": service.image,
					"category": service.category,
					"subcategory": service.subcategory,
				}
			)

	formbasic = UpdateBasicForm(
			initial={
					"basic_name": basic.basic_name, 
					"basic_desc": basic.basic_desc,
					"basic_delivery": basic.basic_delivery,
					"basic_revision": basic.basic_revision,
					"basic_price": basic.basic_price,
				}
			)

	formstandard = UpdateStandardForm(
			initial={
					"standard_name": standard.standard_name, 
					"standard_desc": standard.standard_desc,
					"standard_delivery": standard.standard_delivery,
					"standard_revision": standard.standard_revision,
					"standard_price": standard.standard_price,
				}
			)

	formpremium = UpdatePremiumForm(
			initial={
					"premium_name": premium.premium_name, 
					"premium_desc": premium.premium_desc,
					"premium_delivery": premium.premium_delivery,
					"premium_revision": premium.premium_revision,
					"premium_price": premium.premium_price,
				}
			)

	context['formservice'] = formservice
	context['formbasic'] = formbasic
	context['formstandard'] = formstandard
	context['formpremium'] = formpremium
	context['account'] = account
	context['category'] = category
	context['service'] = service

	return render(request, 'service/edit_service.html', context)

def delete_service_view(request, slug):
	
	context = {}

	service = get_object_or_404(ServicePost, slug=slug)
	service_order = ServiceList.objects.filter(service=service).first()
	user_order = service_order.user
	
	if (service_order.basic_packet is not None):
		basic_order = service_order.basic_packet
		user_order.wallet += int(basic_order.basic_price)
		user_order.save()
		service.delete()
		return redirect("buyerpage")
	elif (service_order.standard_packet is not None):
		standard_order = service_order.standard_packet
		user_order.wallet += int(standard_order.standard_price)
		service.delete()
		service.delete()
		return redirect("buyerpage")
	elif (service_order.premium_packet is not None):
		premium_order = service_order.premium_packet
		user_order.wallet += int(premium_order.premium_price)
		user_order.save()
		service.delete()
		return redirect("buyerpage")
