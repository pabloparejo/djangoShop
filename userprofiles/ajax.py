#encoding:utf-8

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from .forms import UserProfileForm, EmailAuthenticationForm

from main.forms import OrderForm

@dajaxice_register
def switchForm(request):
	if request.COOKIES.has_key('form'):
		if request.COOKIES['form'] == "signup":
			form = EmailAuthenticationForm()
			html = form.as_p()

			cookie = "signin"
			title = "Log in"
		else:
			form = UserProfileForm()
			html = form.as_p()

			cookie = "signup"
			title = "Register"

	data = {'content': 	html,
			'cookie': 	cookie,
			'title': 	title}
	return simplejson.dumps(data)

@dajaxice_register
def getOrderForm(request):
	form = OrderForm()
	html = form.as_p()

	return simplejson.dumps({'content': html})