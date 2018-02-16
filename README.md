# django-slackin

Django integration with a public slack organization (inspired by https://github.com/rauchg/slackin).


## Installation & setup

Install django-slackin

```bash
# (coming soon)
# pip install django-slackin
```

Add to your `INSTALLED_APPS`

```python
INSTALLED_APPS = (
    ...
    'slackin',
)
```

Include the django-slackin URLconf in your project urls.py like this

```python
url(r'^slackin/', include('slackin.urls')),
```

Update your settings.py

```python
SLACKIN_TOKEN = 'YOUR-SLACK-TOKEN' # create a token at https://api.slack.com/web
SLACKIN_SUBDOMAIN = 'your-team'    # if https://your-team.slack.com
```

Visit [http://localhost:8000/slackin/](http://localhost:8000/slackin/) to send an invite to your Slack team.


## Using signals

Use signals to listen for invite events. Available signals are:
- email_address_already_invited
- email_address_already_in_team
- sent_invite_to_email_address

To listen for a signal:

```python
from slackin.signals import sent_invite_to_email_address

@receiver(sent_invite_to_email_address)
def my_invite_handler(sender, email_address):
    print 'SIGNAL RECEIVED: {}'.format(email_address)
```

## Custom templates

To use custom templates, add the either of following files to your app's template directory depending on what you want to customize. See [templates/slackin](https://github.com/brilliantorg/django-slackin/tree/master/slackin/templates/slackin) for more details.
- `slackin/invite/page.html`: the surrounding `body`, `head`, and inlined styles
- `slackin/invite/content.html`: the text and form

Templates have access to the following slackin-specific context variables:
- `slackin.team_name`: slack team name
- `slackin.team_image`: slack team image
- `slackin.users_online`: number of team members currently online
- `slackin.users_total`: total number of team members
- `slackin_invite_form`: invite form object
- `slackin_invite_form_success`: `True` if `slackin_invite_form.is_valid()`
