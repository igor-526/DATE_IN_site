from rest_framework.response import Response
from rest_framework.views import APIView
from threading import Thread
from api import config
from api.models import Images
import vk_api
import requests
import asyncio
from api.models import Images
import urllib.request


def uploadtovk_thread(photo, upload:vk_api.VkUpload, counter):
    imgURL = photo.url
    urllib.request.urlretrieve(imgURL, f'file{counter}.jpg')
    # uphoto = upload.photo_messages(peer_id=28964076, photos=photo.url)
    # print(uphoto)


async def uploadtovk(query):
    bot = vk_api.VkApi(token=config.vk_bot_token)
    upload = vk_api.VkUpload(bot)
    counter = 0
    for photo in query:
        counter+=1
        thread = Thread(target=uploadtovk_thread, args=(photo, upload, counter))
        thread.run()


# Create your views here.
class VKPhoto(APIView):
    def post(self, request):
        if request.data.get('auth_token') == '3611810700':
            query = Images.objects.filter(profile_id=request.data.get('id'))
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(uploadtovk(query))
            return Response({'status': 'OK'})
        else:
            return Response({'status': 'Token invalid'})