#encoding:utf-8
from django.contrib import admin
from main.models import Bike, Book, Music, BikeOrder, BookOrder, MusicOrder, Order

# Register your models here.

class BikeAdmin(admin.ModelAdmin):
	exclude = ('category',)
	fieldsets = [
		('Info',	{'fields': ['name', 'description', 'price']}),
		('Popularity', {'fields': ['featured', 'popularity']}),
		('Multimedia', {'fields': ['multimedia', 'preview']}),
	]
	list_display = ('name', 'pub_date', 'price', 'featured', 'popularity')

class BookAdmin(admin.ModelAdmin):
	exclude = ('category',)
	fieldsets = [
		('Info',	{'fields': ['name', 'description', 'price']}),
		('Popularity', {'fields': ['featured', 'popularity']}),
		('Multimedia', {'fields': ['multimedia']}),
	]
	list_display = ('name', 'pub_date', 'price', 'featured', 'popularity')

class MusicAdmin(admin.ModelAdmin):
	exclude = ('category',)
	fieldsets = [
		('Info',	{'fields': ['name', 'description', 'price']}),
		('Popularity', {'fields': ['featured', 'popularity']}),
		('Multimedia', {'fields': ['multimedia', 'preview']}),
	]
	list_display = ('name', 'pub_date', 'price', 'featured', 'popularity')


class BikeInline(admin.TabularInline):
	extra = 1
	model = BikeOrder
	verbose_name = "Bikes in this order"
	verbose_name_plural = "Bikes in order"


class BookInline(admin.TabularInline):
	extra = 1
	model = BookOrder
	verbose_name = "Book in this order"
	verbose_name_plural = "Books in order"


class MusicInline(admin.TabularInline):
	extra = 1
	model = MusicOrder
	verbose_name = "Music in this order"
	verbose_name_plural = "Music in order"


class OrderAdmin(admin.ModelAdmin):

	fieldsets = [
		('Order info',	{	'fields': ['name', 'first_name',\
						 	'total_amount', 'payment',]}),
		('Address',	{'fields': ['street', 'postal_code', 'city']}),
	]
	inlines = [BikeInline, BookInline, MusicInline,]
	list_display = ('__unicode__', 'name', 'first_name',\
					'order_date','address', 'total_amount', 'user')
	list_filter = ('user', 'order_date', 'city')
	search_fields = ('user__username', 'user__email', 'city')



admin.site.register(Bike, BikeAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Music, MusicAdmin)
admin.site.register(Order, OrderAdmin)