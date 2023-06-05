from django.shortcuts import render
from django.views.generic import TemplateView
from api.models import Profile, Settings, Matchlist, Complaintlist, Offerlist
import datetime


class Monitor(TemplateView):
    template_name = 'monitor.html'

    def get(self, request, *args, **kwargs):
        profiles = Profile.objects.all()
        settings = Settings.objects.all()
        offers = Offerlist.objects.all()
        c_p_all = len(profiles)
        c_p_active = 0
        c_p_vk = 0
        c_p_tg = 0
        c_a_hour = 0
        c_a_today = 0
        c_a_yesterday = 0
        c_a_week = 0
        c_o_all = len(offers)
        c_o_not = 0
        c_o_like = 0
        c_o_pass = 0
        matches = Matchlist.objects.count()//2
        complaints = Complaintlist.objects.exclude(cat='report').filter(status='new').count()
        reports = Complaintlist.objects.filter(cat='report', status='new').count()
        for pr in profiles:
            if pr.status == 'active':
                c_p_active += 1
            if pr.vk_id:
                c_p_vk += 1
            if pr.tg_id:
                c_p_tg += 1
        for pr in settings:
            if pr.last_usage + datetime.timedelta(hours=1) >= datetime.datetime.now(tz=datetime.timezone.utc):
                c_a_hour += 1
            if pr.last_usage.date() == datetime.date.today():
                c_a_today += 1
            if pr.last_usage.date() == datetime.date.today()-datetime.timedelta(days=1):
                c_a_yesterday += 1
            if pr.last_usage.date() <= datetime.date.today()-datetime.timedelta(days=7):
                c_a_week += 1
        for of in offers:
            if of.status == 'not_offered':
                c_o_not += 1
            if of.status == 'pass':
                c_o_pass += 1
            if of.status == 'like':
                c_o_like += 1
        context = {'pr_all': c_p_all, 'pr_active': c_p_active, 'pr_tg': c_p_tg, 'pr_vk': c_p_vk,
                   'ac_hour': c_a_hour, 'ac_today': c_a_today, 'ac_yesterday': c_a_yesterday, 'ac_week': c_a_week,
                   'of_all': c_o_all, 'of_not': c_o_not, 'of_like': c_o_like, 'of_pass': c_o_pass,
                   'matches': matches, 'comps': complaints, 'reports': reports}

        return render(request, self.template_name, context)
