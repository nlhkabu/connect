from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^map$', 'discover.views.map', name='map'),
)
