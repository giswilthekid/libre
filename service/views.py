from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

from service.models import ServicePost, BasicPacket, StandardPacket, PremiumPacket
from blog.models import Category, SubCategory
from account.models import Account, ProjectList

from service.forms import CreateServicePostForm, BasicPacketForm, StandardPacketForm, PremiumPacketForm

@login_required
def sellerpage(request):

	context = {}
	user = request.user
	account = Account.objects.filter(email=request.user.email).first()

	context['account'] = account

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