from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from connect.discover import views

urlpatterns = patterns('',
    url(_(r'^map/$'), views.member_map, name='map'),
)
