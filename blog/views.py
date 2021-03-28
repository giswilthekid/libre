from django.shortcuts import render
from django.http import HttpResponse

def landingpage(request):
	return render(request, 'blog/landingpage.html', {'title': 'Landing Page'})