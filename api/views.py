from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class VKPhoto(APIView):
    def post(self, request):
        if request.data.get('auth_token') == '3611810700':
            return Response({'status': 'OK'})
        else:
            return Response({'status': 'Token invalid'})