from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	return render(request, 'blog/home.html', {'title': 'Home'})

def register(request):
	return render(request, 'blog/register.html', {'title': 'Register'})

def login(request):
	return render(request, 'blog/login.html', {'title': 'Login'})