from rest_framework.response import Response
from rest_framework.views import APIView
from api.utils import do_offers
import asyncio
from api.models import Images
from automatic.tasks import upload_to_vk


class VKPhoto(APIView):
    def post(self, request):
        if request.data.get('auth_token') == 'sdgbste4h6tr46s45fd416s54t86h465fd4ths65g46s5ty4j65rtf5g':
            query = Images.objects.filter(profile_id=request.data.get('id'))
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            upload_to_vk.delay(query)
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
