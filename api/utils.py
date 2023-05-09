from api import config
from api.models import Images
from vkwave.bots import SimpleLongPollBot
from vkwave.bots.utils import PhotoUploader
import requests


def uploadtovk(profile_id):
    bot = SimpleLongPollBot(tokens=config.vk_bot_token, group_id=config.group_id)
    query = Images.objects.filter(Images.profile == profile_id).all()
    print(query)