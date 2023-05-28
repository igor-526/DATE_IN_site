from django.urls import path
from .views import VKPhoto, DoOfferList

apiurlpatterns = [
    path('v1/vkphoto/', VKPhoto.as_view()),
    path('v1/do_offers/', DoOfferList.as_view()),
]