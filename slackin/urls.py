from django.conf.urls import url

from slackin.views import SlackinInviteView

urlpatterns = [
    url(r'^$', SlackinInviteView.as_view(), name='slackin_invite'),
]
