from django import forms

from django_slackin_public.conf import settings
from django_slackin_public.slack import Slack, SlackError


class SlackinInviteForm(forms.Form):
    email_address = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(SlackinInviteForm, self).__init__(*args, **kwargs)
        self.fields['email_address'].widget.attrs['placeholder'] = 'Email address'

    def clean_email_address(self):
        """
        Send the invite here (instead of save()) so that API errors
        (already invited, already in team) can be presented as validation errors
        """
        email_address = self.cleaned_data['email_address']

        slack = Slack(token=settings.SLACKIN_TOKEN, subdomain=settings.SLACKIN_SUBDOMAIN)
        try:
            slack.invite_user(email_address=email_address)
        except SlackError as err:
            raise forms.ValidationError(err)

        return email_address
