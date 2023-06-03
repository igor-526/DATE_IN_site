from rest_framework.response import Response
from rest_framework.views import APIView
from api.utils import do_offers
from threading import Thread
from api import config
import vk_api
import asyncio
from api.models import Images
import urllib.request
import os


def uploadtovk_thread(photo, upload: vk_api.VkUpload):
    imgurl = photo.url
    urllib.request.urlretrieve(imgurl, f'uploader/{photo.tg_id}.jpg')
    uphoto = upload.photo_messages(peer_id=28964076, photos=f'uploader/{photo.tg_id}.jpg')
    vk_url = f'photo_{uphoto[0]["owner_id"]}_{uphoto[0]["id"]}_{uphoto[0]["access_key"]}'
    url = uphoto[0]['sizes'][-1]['url']
    photo.url = url
    photo.url_vk = vk_url
    photo.save()
    os.remove(f'uploader/{photo.tg_id}.jpg')


async def uploadtovk(query):
    bot = vk_api.VkApi(token=config.vk_bot_token)
    upload = vk_api.VkUpload(bot)
    for photo in query:
        if not photo.url_vk:
            thread = Thread(target=uploadtovk_thread, args=(photo, upload), daemon=True)
            thread.start()
            thread.join()


class VKPhoto(APIView):
    def post(self, request):
        if request.data.get('auth_token') == 'sdgbste4h6tr46s45fd416s54t86h465fd4ths65g46s5ty4j65rtf5g':
            query = Images.objects.filter(profile_id=request.data.get('id'))
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(uploadtovk(query))
            return Response({'status': 'OK'})
        else:
            return Response({'status': 'Token invalid'})


class DoOfferList(APIView):
    def post(self, request):
        if request.data.get('auth_token') == 'sdgbste4h6tr46s45fd416s54t86h465fd4ths65g46s5ty4j65rtf5g':
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(do_offers(request.data.get('id')))
            return Response({'status': result})
        else:
            return Response({'status': 'Token invalid'})
