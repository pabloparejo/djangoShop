#encoding:utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.utils import simplejson
from .models import Bike, Book, Music, BikeOrder, BookOrder, MusicOrder, Order
from django.db.models import Q

from itertools import chain

from .forms import OrderForm
from django.contrib.auth.decorators import login_required

def category(request, category):

	if category == "bikes":
		products = Bike.objects.all()
	elif category == "books":
		products = Book.objects.all()
	else:
		products = Music.objects.all()

	featured_products = products.filter(featured=True)\
						.order_by('-pub_date')[:8]
	products = {'css_class': category + '-products showcase', \
				'name': 'Products', 'products': products}
	featured_products = {	'css_class': 'featured-products',\
							'name': 'Featured Products',\
							'products': featured_products}

	page_class = 'showcase ' + category
	page_title = category

	product_sections = [featured_products, products]
	return render(request, 'showcase.html', locals())



def saveOrderProducts(order_content, order):

	amount = 0
	prod_error = False

	for product in order_content:
		product_uid = product['id'].split("-")

		category = product_uid[0]
		p_id = product_uid[1]
		quantity = product['quantity']
		p_price = product['price'].split(' ')[0]
		p_price = p_price.replace(',','.')
		amount += float(p_price) * float(quantity)

		if category == 'bikes':
			bike_obj = Bike.objects.get(pk=p_id)
			bike_obj.popularity += (1*quantity)
			bike_obj.save()
			prod_order = order.bikeorder_set.create(product=bike_obj,
													quantity=quantity)
		elif category == 'books':
			book_obj = Book.objects.get(pk=p_id)
			book_obj.popularity += (1*quantity)
			book_obj.save()
			prod_order = order.bookorder_set.create(product=book_obj,
													quantity=quantity)
		elif category == 'music':
			music_obj = Music.objects.get(pk=p_id)
			music_obj.popularity += (1*quantity)
			music_obj.save()
			prod_order = order.musicorder_set.create(	product=music_obj,
														quantity=quantity)
		else:
			prod_error = True
			print "product error"
		if not prod_error:
			prod_order.save()
	return amount



@login_required(login_url='/sign')
def checkOut(request):
	if request.method == "POST":
		form = OrderForm(request.POST)
		if form.is_valid():
			user = request.user
			order_content = simplejson.loads(request.POST['cartJSONdata'])
			order = form.save(commit=False)
			order.user = user
			order.total_amount = 0
			order.save()
			order.total_amount = saveOrderProducts(order_content, order)
			order.save()

			bikes = BikeOrder.objects.filter(order=order) 
			books = BookOrder.objects.filter(order=order) 
			music = MusicOrder.objects.filter(order=order) 

			products = list(chain(bikes, books, music))
			page_class = 'checkout-page'
			page_title = "Order done!"

			response = render(request, 'success.html', locals())
			
			return response
	else:
		form = OrderForm()

	page_class = 'checkout-page'
	page_title = "Check out"
	return render(request, 'order.html', locals())


def home(request):
	bikes = {'name': 'bikes'}
	books = {'name': 'books'}
	music = {'name': 'music'}

	bikes['products'] = Bike.objects.order_by('-pub_date')[:3]
	books['products']  = Book.objects.order_by('-pub_date')[:3]
	music['products']  = Music.objects.order_by('-pub_date')[:3]


	page_title = 'home'
	page_class = 'showcase home'

	product_sections = [bikes, books, music]
	return render(request, 'showcase.html', locals())

def product(request, category, p_id):

	if category == "bikes":
		products = Bike.objects.all()
	elif category == "books":
		products = Book.objects.all()
	else:
		products = Music.objects.all()

	
	product = products.get(pk=p_id)
	product.popularity += 1
	product.save()

	products = products.exclude(pk=p_id)

	for p in products:
		if p.popularity > 0:
			p.popularity -= 1
			p.save();

	products = products.order_by('popularity')[:4]

	related = {'title': "Related products", "products": products}

	page_title = product.name
	page_class = 'single-product-page'

	return render(request, 'product.html', locals())


def search(request):

	search = {'error': True, 'hasQuery': False}

	bikes = {'name': 'bikes', 'products': ''}
	books = {'name': 'books', 'products': ''}
	music = {'name': 'music', 'products': ''}

	query = request.GET.get('q', '')
	if query:
		search['hasQuery'] = True
		qset1 = (
			Q(name__icontains=query) |
			Q(description__icontains=query)
			)
		bikes['products'] = Bike.objects.filter(qset1).distinct()\
							.order_by('popularity')
		books['products'] = Book.objects.filter(qset1).distinct()\
							.order_by('popularity')
		music['products'] = Music.objects.filter(qset1).distinct()\
							.order_by('popularity')

	if 	not bikes['products'] and \
		not books['products'] and \
		not music['products'] :

		bikes['products'] = Bike.objects.order_by('popularity')[:3]
		books['products'] = Book.objects.order_by('popularity')[:3]
		music['products'] = Music.objects.order_by('popularity')[:3]
		search['hasOtherProducts'] = True
		
	else:
		search['error'] = False
	
	product_sections = [bikes, books, music]
	page_title = query

	page_class = 'showcase search'

	return render(request, 'showcase.html', locals())



