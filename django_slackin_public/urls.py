from django.conf.urls import url

from django_slackin_public.views import SlackinInviteView

urlpatterns = [
    url(r'^$', SlackinInviteView.as_view(), name='slackin_invite'),
]
