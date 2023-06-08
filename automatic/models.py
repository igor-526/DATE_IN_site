from django.db import models


class Messages(models.Model):
    vk_id = models.BigIntegerField(null=True)
    tg_id = models.BigIntegerField(null=True)
    cat = models.CharField(null=False)
    message = models.CharField(null=False)