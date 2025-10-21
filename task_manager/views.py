from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'index.html'

    GREETING = _('Првиетсвуем в Хекслет!')
    HEADING = _('Практические курсы программирования')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['greeting'] = self.GREETING
        context['heading'] = self.HEADING
        return context

class CustomLogoutView(LogoutView):
    next_page = '/'  # редирект после выхода
    LOGGRD_OUT = _('Вы разлогинены')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, self.LOGGRD_OUT)
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_message = _('Вы залогинены')