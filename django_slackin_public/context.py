import typing

from django.core.cache import cache

from django_slackin_public.conf import settings
from django_slackin_public.slack import Slack, SlackError


class Context(typing.NamedTuple):
    team_name: str = 'unknown'
    team_image: str = ''
    users_online: int = -1
    users_total: int = -1


def is_real_slack_user(member):
    return not (member.get('id') == 'USLACKBOT' or member.get('is_bot') or member.get('deleted'))


class ContextBuilder(object):
    CACHE_KEY = 'SLACK_CACHE'
    CACHE_PERIOD = 3600
    DEFAULT_RETRY_AFTER = 10

    def __init__(self):
        self._api = Slack(settings.SLACKIN_TOKEN)

    def fetch(self):
        data = cache.get(self.CACHE_KEY)
        if data is None:
            try:
                data = self._fetch()
            except SlackError as err:
                data = self._fallback_context()
                timeout = err.retry_after or self.DEFAULT_RETRY_AFTER
            else:
                timeout = self.CACHE_PERIOD

            cache.set(self.CACHE_KEY, data, timeout=timeout)
        return data

    def _fallback_context(self):
        return dict(
            team_name=settings.SLACKIN_SUBDOMAIN,
            team_image='',
            users_online=-1,
            users_total=-1,
        )

    def _fetch(self):
        team_response = self._api.get_team()

        users_response = self._api.get_users()
        users = [member for member in users_response['members'] if is_real_slack_user(member)]
        users_online = [user for user in users if user.get('presence') == 'active']

        return dict(
            team_name=team_response['team']['name'],
            team_image=team_response['team']['icon']['image_132'],
            users_online=len(users_online),
            users_total=len(users),
        )
