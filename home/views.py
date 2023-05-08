from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, self.template_name, context)
