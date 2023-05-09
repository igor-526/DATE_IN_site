from django.db import models


class Profile(models.Model):
    phone = models.IntegerField(null=True, unique=True)
    vk_id = models.IntegerField(null=True, unique=True)
    tg_id = models.IntegerField(null=True, unique=True)
    tg_nick = models.CharField(null=True)
    tg_url = models.CharField(null=True)
    name = models.CharField(null=False)
    bdate = models.DateField(null=False)
    sex = models.IntegerField(null=False)
    city = models.CharField(null=True)
    geo_lat = models.FloatField(null=False)
    geo_long = models.FloatField(null=False)
    description = models.CharField(null=True)
    status = models.CharField(null=False)


class Settings(models.Model):
    age_min = models.IntegerField(null=False)
    age_max = models.IntegerField(null=False)
    find_m = models.IntegerField(null=False)
    find_f = models.IntegerField(null=False)
    purp1 = models.IntegerField(null=False)
    purp2 = models.IntegerField(null=False)
    purp3 = models.IntegerField(null=False)
    purp4 = models.IntegerField(null=False)
    purp5 = models.IntegerField(null=False)
    ch_name = models.DateTimeField(null=True)
    ch_sex = models.DateTimeField(null=True)
    ch_bdate = models.DateTimeField(null=True)
    created = models.DateField(null=False)
    deactivated = models.DateTimeField(null=True)
    last_usage = models.DateTimeField(null=False)
    offer_kilometrage = models.IntegerField(null=True)
    offer_ofset = models.IntegerField(null=True)


class Images(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False, related_name='of_profile')
    url = models.CharField(null=True)
    url_vk = models.CharField(null=True)
    tg_id = models.CharField(null=True)
    description = models.CharField(null=False)


class Offerlist(models.Model):
    profile = models.IntegerField(null=False)
    offer_id = models.IntegerField(null=False)
    status = models.CharField(null=False)


class Matchlist(models.Model):
    profile_1 = models.IntegerField(null=False)
    profile_2 = models.IntegerField(null=False)


class Complaintlist(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False, related_name='profile_of')
    complain_to = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False, related_name='profile_to')
    cat = models.CharField(null=False)
    description = models.CharField(null=True)
    images = models.CharField(null=True)
    status = models.CharField(null=False)
    date = models.DateTimeField(null=False)

