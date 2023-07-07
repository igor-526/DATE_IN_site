"""
URL configuration for datein project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.urls import apiurlpatterns
from home.views import Home, Rules, About, Privacy
from articles.views import AllArticles

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(apiurlpatterns)),
    path('', Home.as_view()),
    path('info/rules/', Rules.as_view()),
    path('info/about/', About.as_view()),
    path('info/privacy/', Privacy.as_view()),
    path('articles/', AllArticles.as_view()),
]
