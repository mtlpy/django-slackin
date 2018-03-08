import unittest

from django.test import Client

import requests_mock


class SimpleTest(unittest.TestCase):
    def _call(self):
        response = Client().get('/slackin')
        self.assertEqual(response.status_code, 200)
        return response

    def test_nominal(self):
        with requests_mock.mock() as m:
            m.post('//slack.com/api/team.info', json=TEAM_INFO_RESPONSE)
            m.post('//slack.com/api/users.list', json=USERS_LIST_RESPONSE)

            response = self._call()

        self.assertIn(
            b'<strong>0</strong> users online now of <strong>2</strong> registered.',
            response.content,
        )

    def test_throttled(self):
        with requests_mock.mock() as m:
            m.post('//slack.com/api/team.info', json=RATE_LIMITED_RESPONSE, status_code=429)
            m.post('//slack.com/api/users.list', json=RATE_LIMITED_RESPONSE, status_code=429)

            response = self._call()

        self.assertIn(
            b'<strong>-1</strong> users online now of <strong>-1</strong> registered.',
            response.content,
        )


RATE_LIMITED_RESPONSE = {
    'ok': False,
    'error': 'ratelimited',
    'headers': {
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': '34',
        'Connection': 'keep-alive',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'private, no-cache, no-store, must-revalidate',
        'Date': 'Thu, 08 Mar 2018 02:19:26 GMT',
        'Expires': 'Mon, 26 Jul 1997 05:00:00 GMT',
        'Pragma': 'no-cache',
        'Referrer-Policy': 'no-referrer',
        'Retry-After': '9',
        'Server': 'Apache',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
        'X-Content-Type-Options': 'nosniff',
        'X-OAuth-Scopes': 'identify,read,post,client,apps,admin',
        'X-Slack-Backend': 'h',
        'X-Slack-Req-Id': 'ba437519-e114-49fd-99ae-ff30de936b6d',
        'X-XSS-Protection': '0',
        'X-Cache': 'Error from cloudfront',
        'Via': '1.1 5f0ff016085532665645d41b997a1c90.cloudfront.net (CloudFront)',
        'X-Amz-Cf-Id': 'EmRATI3hHeGMYiw-MNiG0FhGO79ZkAPz0fYYzrSaDTHbxHk_y7K4pw==',
    },
}

TEAM_INFO_RESPONSE = {
    'ok': True,
    'team': {
        'id': 'T12345',
        'name': 'My Team',
        'domain': 'example',
        'email_domain': 'example.com',
        'icon': {
            'image_34': 'https:\/\/...',
            'image_44': 'https:\/\/...',
            'image_68': 'https:\/\/...',
            'image_88': 'https:\/\/...',
            'image_102': 'https:\/\/...',
            'image_132': 'https:\/\/...',
            'image_default': True
        },
        'enterprise_id': 'E1234A12AB',
        'enterprise_name': 'Umbrella Corporation'
    }
}

USERS_LIST_RESPONSE = {
    'ok': True,
    'members': [
        {
            'id': 'W012A3CDE',
            'team_id': 'T012AB3C4',
            'name': 'spengler',
            'deleted': False,
            'color': '9f69e7',
            'real_name': 'spengler',
            'tz': 'America\/Los_Angeles',
            'tz_label': 'Pacific Daylight Time',
            'tz_offset': -25200,
            'profile': {
                'avatar_hash': 'ge3b51ca72de',
                'status_text': 'Print is dead',
                'status_emoji': ':books:',
                'real_name': 'Egon Spengler',
                'display_name': 'spengler',
                'real_name_normalized': 'Egon Spengler',
                'display_name_normalized': 'spengler',
                'email': 'spengler@ghostbusters.example.com',
                'image_24': 'https:\/\/...\/avatar\/e3b51ca72dee4ef87916ae2b9240df50.jpg',
                'image_32': 'https:\/\/...\/avatar\/e3b51ca72dee4ef87916ae2b9240df50.jpg',
                'image_48': 'https:\/\/...\/avatar\/e3b51ca72dee4ef87916ae2b9240df50.jpg',
                'image_72': 'https:\/\/...\/avatar\/e3b51ca72dee4ef87916ae2b9240df50.jpg',
                'image_192': 'https:\/\/...\/avatar\/e3b51ca72dee4ef87916ae2b9240df50.jpg',
                'image_512': 'https:\/\/...\/avatar\/e3b51ca72dee4ef87916ae2b9240df50.jpg',
                'team': 'T012AB3C4'
            },
            'is_admin': True,
            'is_owner': False,
            'is_primary_owner': False,
            'is_restricted': False,
            'is_ultra_restricted': False,
            'is_bot': False,
            'updated': 1502138686,
            'is_app_user': False,
            'has_2fa': False
        },
        {
            'id': 'W07QCRPA4',
            'team_id': 'T0G9PQBBK',
            'name': 'glinda',
            'deleted': False,
            'color': '9f69e7',
            'real_name': 'Glinda Southgood',
            'tz': 'America\/Los_Angeles',
            'tz_label': 'Pacific Daylight Time',
            'tz_offset': -25200,
            'profile': {
                'avatar_hash': '8fbdd10b41c6',
                'image_24': 'https:\/\/a.slack-edge.com...png',
                'image_32': 'https:\/\/a.slack-edge.com...png',
                'image_48': 'https:\/\/a.slack-edge.com...png',
                'image_72': 'https:\/\/a.slack-edge.com...png',
                'image_192': 'https:\/\/a.slack-edge.com...png',
                'image_512': 'https:\/\/a.slack-edge.com...png',
                'image_1024': 'https:\/\/a.slack-edge.com...png',
                'image_original': 'https:\/\/a.slack-edge.com...png',
                'first_name': 'Glinda',
                'last_name': 'Southgood',
                'title': 'Glinda the Good',
                'phone': '',
                'skype': '',
                'real_name': 'Glinda Southgood',
                'real_name_normalized': 'Glinda Southgood',
                'display_name': 'Glinda the Fairly Good',
                'display_name_normalized': 'Glinda the Fairly Good',
                'email': 'glenda@south.oz.coven'
            },
            'is_admin': True,
            'is_owner': False,
            'is_primary_owner': False,
            'is_restricted': False,
            'is_ultra_restricted': False,
            'is_bot': False,
            'updated': 1480527098,
            'has_2fa': False
        }
    ],
    'cache_ts': 1498777272,
    'response_metadata': {
        'next_cursor': 'dXNlcjpVMEc5V0ZYTlo='
    }
}
