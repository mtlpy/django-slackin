from django.shortcuts import render
from django.views.generic.base import View

from django_slackin_public.context import ContextBuilder
from django_slackin_public.forms import SlackinInviteForm


class SlackinInviteView(View):
    template_name = 'slackin/invite/page.html'

    def get_generic_context(self):
        return {
            'slackin': ContextBuilder().fetch(),
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
