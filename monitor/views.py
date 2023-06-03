from django.shortcuts import render
from django.views.generic import TemplateView
from api.models import Profile, Settings, Matchlist, Complaintlist
import datetime


class Monitor(TemplateView):
    template_name = 'monitor.html'

    def get(self, request, *args, **kwargs):
        setts = Settings.objects.all()
        matches = Matchlist.objects.count()
        compls = Complaintlist.objects.count()
        counttoday = 0
        countweek = 0
        for usr in setts:
            print(usr.last_usage)
            if usr.last_usage.date() == datetime.date.today():
                counttoday += 1
            if usr.last_usage.date() < datetime.date.today() - datetime.timedelta(hours=1):
                countweek += 1
        context = {'usrs': len(setts), 'today': counttoday, 'week': countweek, 'matches': matches//2, 'compls': compls}

        return render(request, self.template_name, context)
