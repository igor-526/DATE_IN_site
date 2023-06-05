from api.models import Offerlist, Profile
from haversine import haversine
import datetime
from random import randint


def sort_dist(offer):
    return offer['dist']


async def do_offers(p_id):
    prof_for = Profile.objects.filter(id=p_id).first()
    prof_offerlist = Offerlist.objects.filter(profile=p_id)
    offered_ids = [of.offer_id for of in prof_offerlist]
    today_date = datetime.date.today()
    bdate_max = today_date.replace(year=today_date.year-prof_for.sets.age_min)
    bdate_min = today_date.replace(year=today_date.year-prof_for.sets.age_max)
    prof_geo = (prof_for.geo_lat, prof_for.geo_long)
    if prof_for.sets.find_f == 1 and prof_for.sets.find_m == 1:
        sex = [1, 2]
    else:
        sex = [1] if prof_for.sets.find_f == 1 else [2]
    counter = 0
    while counter != 5:
        if prof_for.sex == 2:
            offerlist = Profile.objects.filter(bdate__lte=bdate_max,
                                               bdate__gte=bdate_min,
                                               sex__in=sex,
                                               sets__find_m=1,
                                               status='active',
                                               sets__last_usage__date__gte=datetime.date.today()-datetime.timedelta(
                                                   days=7)).exclude(id=p_id).count()
            limit = offerlist // 100 * 10
            offset = randint(0, offerlist - limit)
            offerlist = Profile.objects.filter(bdate__lte=bdate_max,
                                               bdate__gte=bdate_min,
                                               sex__in=sex,
                                               sets__find_m=1,
                                               status='active',
                                               sets__last_usage__date__gte=datetime.date.today() - datetime.timedelta(
                                                   days=7)).exclude(id=p_id)[limit:offset]
            if offerlist:
                break
            else:
                counter += 1
        else:
            offerlist = Profile.objects.filter(bdate__lte=bdate_max,
                                               bdate__gte=bdate_min,
                                               sex__in=sex,
                                               sets__find_f=1,
                                               status='active',
                                               sets__last_usage__date__gte=datetime.date.today() - datetime.timedelta(
                                                   days=7)).exclude(id=p_id).count()
            limit = offerlist // 100 * 10
            offset = randint(0, offerlist - limit)
            offerlist = Profile.objects.filter(bdate__lte=bdate_max,
                                               bdate__gte=bdate_min,
                                               sex__in=sex,
                                               sets__find_f=1,
                                               status='active',
                                               sets__last_usage__date__gte=datetime.date.today() - datetime.timedelta(
                                                   days=7)).exclude(id=p_id)[limit:offset]
            if offerlist:
                break
            else:
                counter += 1
    offers = []
    for offer in offerlist:
        if offer.id not in offered_ids:
            offer_geo = (offer.geo_lat, offer.geo_long)
            dist = haversine(prof_geo, offer_geo)
            if prof_for.sets.km_limit >= dist:
                offers.append({'profile': offer, 'dist': dist})
    if len(offers) == 0:
        return 'no_profiles'
    offers = sorted(offers, key=sort_dist)
    for prof in offers:
        Offerlist.objects.create(profile=prof_for, offer=prof['profile'], dist=prof['dist'],
                                 date=datetime.date.today(), status='not_offered')
    return 'ready'
