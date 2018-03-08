import logging

from slackclient import SlackClient

from django_slackin_public.signals import (
    email_address_already_invited,
    email_address_already_in_team,
    sent_invite_to_email_address
)

log = logging.getLogger(__name__)


class SlackError(Exception):
    pass


class SlackThrottledCall(SlackError):
    def __init__(self, retry_after):
        self.retry_after = retry_after
        super().__init__()


def check_for_error(response, params):
    error_code = response.get('error')

    if not error_code:
        return

    # generic errors
    if error_code == 'not_authed':
        raise SlackError('Missing Slack token. Please contact an administrator.')
    elif error_code == 'invalid_auth':
        raise SlackError('Invalid Slack token. Please contact an administrator.')
    elif error_code == 'account_inactive':
        raise SlackError('Slack token is inactive. Please contact an administrator.')
    elif error_code == 'ratelimited':
        retry_after = response["headers"].get("Retry-After")
        raise SlackThrottledCall(retry_after)

    # invite errors
    elif error_code == 'missing_scope':
        raise SlackError('Slack token is for a non-admin user. Please contact an administrator.')
    elif error_code == 'already_invited':
        if 'email' in params:
            email_address = params['email']
            email_address_already_invited.send(sender=Slack, email_address=email_address)
            raise SlackError('{} has already been invited.'.format(email_address))
        else:
            raise SlackError('That email address has already been invited.')
    elif error_code == 'already_in_team':
        if 'email' in params:
            email_address = params['email']
            email_address_already_in_team.send(sender=Slack, email_address=email_address)
            raise SlackError('{} is already in this team.'.format(email_address))
        else:
            raise SlackError('That email address is already in this team.')
    elif error_code == 'paid_teams_only':
        raise SlackError('{} {}'.format(
            'Ultra-restricted invites are only available for paid accounts.',
            'Please contact an administrator.'))

    else:
        raise SlackError('Unknown error: {}'.format(error_code))


class Slack(object):
    def __init__(self, token):
        self._client = SlackClient(token)

    def _call(self, method, **params):
        response = self._client.api_call(method, **params)
        log.info('Slack client received: %s', response)

        try:
            check_for_error(response, params)
        except Exception as exc:
            log.error("Slack API call failed", exc_info=exc)
            raise

        return response

    def get_team(self):
        return self._call('team.info')

    def get_users(self):
        return self._call('users.list', presence=1)

    def invite_user(self, email_address):
        response = self._call('users.admin.invite', email=email_address)
        sent_invite_to_email_address.send(sender=self.__class__, email_address=email_address)
        return response
