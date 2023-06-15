from api.models import Offerlist, Profile, Matchlist
from haversine import haversine
import datetime
from random import randint


def sort_dist(offer):
    return offer['dist']


async def do_offers(p_id):
    prof_for = Profile.objects.filter(id=p_id).first()
    prof_offerlist = Offerlist.objects.filter(profile=p_id)
    offered_ids = [of.offer_id for of in prof_offerlist]
    offered_ids.append(p_id)
    matchlist = Matchlist.objects.filter(profile_1=p_id).exclude(profile_2__in=offered_ids)
    matchlist_ids = [pr.profile_2 for pr in matchlist]
    liked = Offerlist.objects.filter(offer=p_id, status='like').exclude(profile__in=matchlist_ids)
    liked_ids = [pr.profile for pr in liked]
    for lid in liked_ids:
        offered_ids.append(lid.id)
    today_date = datetime.date.today()
    bdate_max = today_date.replace(year=today_date.year-prof_for.sets.age_min)
    bdate_min = today_date.replace(year=today_date.year-prof_for.sets.age_max)
    prof_geo = (prof_for.geo_lat, prof_for.geo_long)
    if prof_for.sets.find_f == 1 and prof_for.sets.find_m == 1:
        sex = [1, 2]
    else:
        sex = [1] if prof_for.sets.find_f == 1 else [2]
    counter = 0
    if prof_for.sex == 1:
        find_f = [1]
        find_m = [0, 1]
    else:
        find_f = [0, 1]
        find_m = [1]
    while counter != 5:
        print(offered_ids)
        offerlist = Profile.objects.filter(bdate__lte=bdate_max,
                                           bdate__gte=bdate_min,
                                           sex__in=sex,
                                           sets__find_m__in=find_m,
                                           sets__find_f__in=find_f,
                                           status='active',
                                           sets__last_usage__date__gte=datetime.date.today()-datetime.timedelta(
                                                   days=7)).exclude(id__in=offered_ids).count()
        limit = offerlist // 100 * 10
        offset = randint(0, offerlist - limit)
        offerlist = Profile.objects.filter(bdate__lte=bdate_max,
                                           bdate__gte=bdate_min,
                                           sex__in=sex,
                                           sets__find_m__in=find_m,
                                           sets__find_f__in=find_f,
                                           status='active',
                                           sets__last_usage__date__gte=datetime.date.today() - datetime.timedelta(
                                                   days=7)).exclude(id__in=offered_ids)[limit:offset]
        if offerlist:
            break
        else:
            counter += 1
    offers = []
    for offer in offerlist:
        if liked_ids:
            if randint(0, 100) <= 20:
                offers.append({'profile': liked_ids[0], 'dist': 0})
                liked_ids.pop(0)
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
