from django.conf.urls import patterns, url

from djraspya import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

)
