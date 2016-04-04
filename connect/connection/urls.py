from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from connect.connection import views

urlpatterns = patterns(
    '',
    url(_(r'^connect-with-user/(?P<user_id>\d+)/$'), views.connect_with_user, name='connect-with-user'),
)
