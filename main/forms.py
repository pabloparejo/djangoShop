from django.forms import ModelForm
from django import forms
from main.models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'id', 'total_amount')
        fields = ( 	'name', 'first_name', 'street', \
        			'postal_code', 'city', 'payment')