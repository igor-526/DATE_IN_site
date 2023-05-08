from django.urls import path
from .views import VKPhoto

apiurlpatterns = [
    path('v1/vkphoto/', VKPhoto.as_view()),
]