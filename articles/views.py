import datetime

from django.shortcuts import render
from django.views.generic import TemplateView

class AllArticles(TemplateView):
    template_name = 'articles.html'

    def get(self, request, *args, **kwargs):
        title = 'Правила безопасного знакомства:'
        text = 'Миллионы людей пользуются сайтами знакомств ежедневно, поэтому важно помнить о том, как безопасно знакомиться в сети:'
        date = datetime.date.today()
        owner = 'Екатерина'
        c = [{'title': title, 'text': text, 'owner': owner, 'date': date},
             {'title': title, 'text': text, 'owner': owner, 'date': date},
             {'title': title, 'text': text, 'owner': owner, 'date': date}]
        context = {'articles': c}

        return render(request, self.template_name, context)