from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect

from .forms import UserProfileForm, EmailAuthenticationForm
from main.models import Order

def signin(request):
	form = EmailAuthenticationForm(request.POST or None)
	sign_title = "Log in"
	if form.is_valid():
		login(request, form.get_user())
		response = HttpResponseRedirect('/')
		response.delete_cookie('form')
		return response
	change_to_form = "Register"
	page_class = 'login'
	response = render(request, 'sign.html', locals())
	response.set_cookie('form', 'signin')
	return response


def signDispatcher(request):

	if 	request.user.is_authenticated():
		user = request.user
		recentOrders = Order.objects.filter(user=user)
		recentOrders = recentOrders.order_by('-order_date')[:6]
		page_title = user.username
		return render(request, 'user_info.html', locals())
	else:
		form = EmailAuthenticationForm(request.POST)
		if form.is_valid():
			login(request, form.get_user())
			response = HttpResponseRedirect('/')
			response.set_cookie('hasRegistered', True)
			response.delete_cookie('form')
			return response
		if request.COOKIES.has_key('hasRegistered'):
			if request.COOKIES['hasRegistered'] == "True":
				return signin(request)
		else:
			page_class = 'signin'
			form = UserProfileForm(request.POST or None)
			sign_title = "Register"
			change_to_form = "log in"
			response = render(request, 'sign.html', locals())
			response.set_cookie('form', "signup")
			if form.is_valid():
				form.save()
				request.POST = "";
				response = signin(request)
				response.set_cookie('hasRegistered', True)


	return response

def userLogOut(request):
	logout(request)
	return HttpResponseRedirect('/')