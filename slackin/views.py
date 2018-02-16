from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.shortcuts import render
from django.views.generic.base import View

from slackin.conf import settings
from slackin.slack import Slack, SlackThrottledCall
from slackin.forms import SlackinInviteForm


def is_real_slack_user(member):
    return not (member.get('id') == 'USLACKBOT' or member.get('is_bot') or member.get('deleted'))


class SlackContext(object):
    CACHE_KEY = 'SLACK_CACHE'
    CACHE_PERIOD = 60
    THROTTLED_CACHE_PERIOD = 5

    def __init__(self):
        self._api = Slack(settings.SLACKIN_TOKEN, settings.SLACKIN_SUBDOMAIN)

    def fetch(self):
        data = cache.get(self.CACHE_KEY)
        if data is None:
            throttled, data = self._fetch()
            timeout = self.THROTTLED_CACHE_PERIOD if throttled else self.CACHE_PERIOD
            cache.set(self.CACHE_KEY, data, timeout=timeout)
        return data

    def _fetch(self):
        context = {}
        throttled = False

        try:
            response = self._api.get_team()
        except SlackThrottledCall:
            context['team_name'] = settings.SLACKIN_SUBDOMAIN
            context['team_image'] = ''
            throttled = True
        else:
            context['team_name'] = response['team']['name']
            context['team_image'] = response['team']['icon']['image_132']

        try:
            response = self._api.get_users()
        except SlackThrottledCall:
            context['users_online'] = -1
            context['users_total'] = -1
            throttled = True
        else:
            users = [member for member in response['members'] if is_real_slack_user(member)]
            users_online = [user for user in users if user.get('presence') == 'active']
            context['users_online'] = len(users_online)
            context['users_total'] = len(users)

        return throttled, context


class SlackinInviteView(View):
    template_name = 'slackin/invite/page.html'

    def get_generic_context(self):
        return {
            'slackin': SlackContext().fetch(),
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
