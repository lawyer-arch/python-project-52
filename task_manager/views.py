from django.shortcuts import render
from django.views import View

class HomePageView(View):
    template_name = 'index.html'
    
    def get(self, request):
        context = {
            'greeting': 'Привет от Хекслета!'
        }
        return render(request, self.template_name, context)
