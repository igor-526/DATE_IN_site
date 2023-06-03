from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, self.template_name, context)


class Rules(TemplateView):
    template_name = 'info.html'

    def get(self, request, *args, **kwargs):
        context = {'infotemp': 'rules.html',
                   'name': 'Правила использования',
                   'menu': [{'name': 'Политика конфиденциальности', 'href': 'privacy'},
                            {'name': 'Что это', 'href': 'about'}]}

        return render(request, self.template_name, context)


class About(TemplateView):
    template_name = 'info.html'

    def get(self, request, *args, **kwargs):
        context = {'infotemp': 'about.html',
                   'name': 'Что такое DATE IN?',
                   'menu': [{'name': 'Политика конфиденциальности', 'href': 'privacy'},
                            {'name': 'Правила использования', 'href': 'rules'}]}

        return render(request, self.template_name, context)


class Privacy(TemplateView):
    template_name = 'info.html'

    def get(self, request, *args, **kwargs):
        context = {'infotemp': 'privacy.html',
                   'name': 'Политика конфиденциальности',
                   'menu': [{'name': 'Правила использования', 'href': 'rules'},
                            {'name': 'Что это', 'href': 'about'}]}

        return render(request, self.template_name, context)