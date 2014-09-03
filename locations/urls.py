from django.conf.urls import patterns, url

from locations import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
	url(r'^locations$', views.locations, name='locations')
)