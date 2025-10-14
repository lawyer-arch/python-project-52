from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "index.html"

    GREETING = _("Првиетсвуем в Хекслет!")
    HEADING = _("Практические курсы программирования")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["greeting"] = self.GREETING
        context["heading"] = self.HEADING
        return context


class CustomLoginView(auth_views.LoginView):
    template_name = "registration/login.html"

    def form_valid(self, form):
        messages.success(self.request, _("Вы залогинены"))
        return super().form_valid(form)


class CustomLogoutView(auth_views.LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _("Вы разлогенены"))
        return super().dispatch(request, *args, **kwargs)
