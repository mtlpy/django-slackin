import time

from django.utils.functional import cached_property
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.cache import cache

from django.shortcuts import render
from django.template import RequestContext

from django.views.generic.base import View

from slackin.conf import settings
from slackin.slack import Slack
from slackin.forms import SlackinInviteForm


class SlackClient(object):
    def __init__(self, token, subdomain):
        self._api = Slack(token=token, subdomain=subdomain)

    def get_team(self):
        response = self._api.get_team()
        data = response['team']
        data['image'] = response['team']['icon']['image_132']
        return {
            'team': data
        }

    def _clean_users(self, users):
        cleaned_users = []
        for user in users:
            if (user.get('id') != 'USLACKBOT'
                    and not user.get('is_bot', False)
                    and not user.get('deleted', False)):
                cleaned_users.append(user)
        return cleaned_users

    def get_users(self):
        response = self._api.get_users()
        users_total = self._clean_users(response['members'])
        users_online = [
            user
            for user in users_total
            if 'presence' in user and user['presence'] == 'active'
        ]
        return {
            'users': users_total,
            'users_online': len(users_online),
            'users_total': len(users_total),
        }


def get_slack_info():
    client = SlackClient(settings.SLACKIN_TOKEN, settings.SLACKIN_SUBDOMAIN)
    return {**client.get_team(), **client.get_users()}


def get_cached_slack_info():
    return cache.get_or_set('SLACK_CACHE', get_slack_info)  # Default timeout: 5 min


class SlackinInviteView(View):
    template_name = 'slackin/invite/page.html'

    def get_generic_context(self):
        return {
            'slackin': get_cached_slack_info(),
            'login_required': settings.SLACKIN_LOGIN_REQUIRED,
        }

    def get_redirect_url(self):
        if '/' in settings.SLACKIN_LOGIN_REDIRECT:
            return settings.SLACKIN_LOGIN_REDIRECT
        else:
            return reverse(settings.SLACKIN_LOGIN_REDIRECT)

    def get(self, request):
        if settings.SLACKIN_LOGIN_REQUIRED and not self.request.user.is_authenticated():
            return HttpResponseRedirect(self.get_redirect_url())

        context = self.get_generic_context()
        email_address = ''
        if self.request.user.is_authenticated():
            email_address = self.request.user.email
        context['slackin_invite_form'] = SlackinInviteForm(
            initial={'email_address': email_address},
            user=self.request.user)
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        if settings.SLACKIN_LOGIN_REQUIRED and not self.request.user.is_authenticated():
            return HttpResponseRedirect(self.get_redirect_url())

        context = self.get_generic_context()
        invite_form = SlackinInviteForm(self.request.POST, user=self.request.user)
        if invite_form.is_valid():
            context['slackin_invite_form_success'] = True
        context['slackin_invite_form'] = invite_form
        return render(request, template_name=self.template_name, context=context)
