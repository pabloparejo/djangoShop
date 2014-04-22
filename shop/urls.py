#encoding:utf-8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Examples:
	url(r'^$', 'main.views.home'),
    (r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')), #DAJAXICE
	url(r'^admin/', include(admin.site.urls)),
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^(bikes|books|music)/$', 'main.views.category', \
			name="category"),
	url(r'^(?P<category>(bikes|books|music))/(?P<p_id>\d{1,})-(.*)/$',\
		 'main.views.product', name="product"),
	url(r'^checkout/$', 'main.views.checkOut',\
	 	name="checkOut"),
	url(r'^logout/$', 'userprofiles.views.userLogOut', name="userLogOut"),
	url(r'^search$', 'main.views.search'),
	url(r'^sign/$', 'userprofiles.views.signDispatcher', name="sign"),
	url(r'^upload/(?P<path>.*)$', 'django.views.static.serve',
					{'document_root':settings.MEDIA_ROOT}),
)

urlpatterns += staticfiles_urlpatterns()
