from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'index.html'
    
    GREETING = _('Hello from Hexlet!')
    HEADING = _('Practical programming courses')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['greeting'] = self.GREETING
        context['heading'] = self.HEADING
        return context
