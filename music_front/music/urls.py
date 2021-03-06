"""music_front URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from music.views import *
from music.buy_views import *

urlpatterns = [
    path('first',index),
    path('products',products),
    path('products_ajax',products_ajax),
    path('FindProductsByPrict',FindProductsByPrict),
    path('single',single),
    path('addcart',addcart),
    path('cart',cart),
    path('delcart',delcart),
    path('buyproduct',buyproduct),
    path('login',login),
    path('cancel',cancel),
    path('addcomment',addcomment)
]
