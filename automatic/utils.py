from random import randint
from api import config
import requests


def send_msgvk(vk_id, message):
    url = "https://api.vk.com/method/messages.send"
    params = {
        "access_token": config.vk_bot_token,
        "v": "5.131",
        "user_id": vk_id,
        "random_id": randint(2000000000, 2147483647),
        "message": message
    }
    requests.get(url, params=params)


def send_msgtg(tg_id, message):
    url = f'https://api.telegram.org/bot{config.tg_bot_token}/sendMessage'
    params = {
        "chat_id": tg_id,
        "text": message
    }
    requests.get(url, params=params)