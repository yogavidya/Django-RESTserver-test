from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

class TestLoginView(LoginView):

    template_name = 'login.html'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = '/o/applications'
        return context

    def login(self, request):
        pass

