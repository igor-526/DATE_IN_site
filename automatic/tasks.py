from datein.celery import app
from api.models import Profile, Settings, Matchlist, Images
from automatic.models import Messages
from automatic.utils import *
import os
import urllib.request
import vk_api
import datetime
from api import config



@app.task
def upload_to_vk(pr_id):
    query = Images.objects.filter(profile_id=pr_id)
    bot = vk_api.VkApi(token=config.vk_bot_token)
    upload = vk_api.VkUpload(bot)
    for photo in query:
        if not photo.url_vk:
            imgurl = photo.url
            urllib.request.urlretrieve(imgurl, f'uploader/{photo.tg_id}.jpg')
            uphoto = upload.photo_messages(peer_id=28964076, photos=f'uploader/{photo.tg_id}.jpg')
            vk_url = f'photo{uphoto[0]["owner_id"]}_{uphoto[0]["id"]}_{uphoto[0]["access_key"]}'
            url = uphoto[0]['sizes'][-1]['url']
            photo.url = url
            photo.url_vk = vk_url
            photo.save()
            os.remove(f'uploader/{photo.tg_id}.jpg')


@app.task
def resetlikes():
    profiles = Profile.objects.all()
    for profile in profiles:
        if profile.limit == 0:
            if profile.tg_id:
                send_msgtg(profile.tg_id, "Теперь снова можно ставить лайки профилям!\n"
                                          "Поищем пару?")
            else:
                send_msgvk(profile.vk_id, "Теперь снова можно ставить лайки профилям!\n"
                                          "Поищем пару?")
        if profile.limit < 30:
            profile.limit = 30
            profile.save()


@app.task
def prepare_messages():
    profiles = Profile.objects.filter(status='active').all()
    for profile in profiles:
        if profile.tg_id and not profile.vk_id:
            Messages.objects.create(tg_id=profile.tg_id, cat='vkremember',
                                    message='А ты знаешь, что у меня есть брат-бот в ВК?\n'
                                            'Там можно зайти в профиль DATE IN через Telegram и продолжить'
                                            'использование, а твой профиль не будет дублироваться. Переходи скорее:\n'
                                            'https://vk.com/im?sel=-220102605')
        if profile.vk_id and not profile.tg_id:
            Messages.objects.create(vk_id=profile.vk_id, cat='tgremember',
                                    message='А ты знаешь, что у меня есть брат-бот в Telegram?\n'
                                            'Там можно зайти в профиль DATE IN через ВК и продолжить использование, '
                                            'а твой профиль не будет дублироваться. Переходи скорее:\n'
                                            'https://t.me/datein_offical_bot')
        if profile.sets.last_usage <= datetime.date.today() - datetime.timedelta(days=7):
            Messages.objects.create(vk_id=profile.vk_id, tg_id=profile.tg_id, cat='usageremember',
                                    message='Тебя не было видно уже больше недели!\n'
                                            'Не забыл обо мне? Сейчас очень хорошее время, чтобы найти себе команию на '
                                            'вечер!')


@app.task
def send_messages():
    messages = Messages.objects.all()
    for message in messages:
        if message.tg_id:
            send_msgtg(message.tg_id, message.message)
        else:
            send_msgvk(message.vk_id, message.message)
        message.delete()


@app.task
def delete_profiles():
    profiles = Profile.objects.filter(status='deactivated',
                                      sets__last_usage__lte=datetime.date.today()-datetime.timedelta(days=7))
    profiles.delete()