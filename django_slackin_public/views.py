from django.core.cache import cache
from django.shortcuts import render
from django.views.generic.base import View

from django_slackin_public.conf import settings
from django_slackin_public.slack import Slack, SlackThrottledCall
from django_slackin_public.forms import SlackinInviteForm


def is_real_slack_user(member):
    return not (member.get('id') == 'USLACKBOT' or member.get('is_bot') or member.get('deleted'))


class SlackContext(object):
    CACHE_KEY = 'SLACK_CACHE'
    CACHE_PERIOD = 3600
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
        }

    def get(self, request):
        context = self.get_generic_context()
        context['slackin_invite_form'] = SlackinInviteForm()
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        context = self.get_generic_context()
        invite_form = SlackinInviteForm(self.request.POST)
        if invite_form.is_valid():
            context['slackin_invite_form_success'] = True
        context['slackin_invite_form'] = invite_form
        return render(request, template_name=self.template_name, context=context)
