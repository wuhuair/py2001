"""music_admin URL Configuration

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
from music.product_views import *
from music.user_views import *
from music.order_views import *
from music.comment_views import *
from music.charts_views import *

urlpatterns = [
    path('to_login',into_login),
    path('login',login),
    path('register',register),
    path('success',success),
    path('index',index),
    path('to_product_type_edit',to_product_type_edit),
    path('product_type_del', product_type_del),
    path('product_type_edit', product_type_edit_or_add),
    path('to_product_type_add', to_product_type_add),
    path('product_list',product_list),
    path('product_del',product_del),
    path('product_batch_del',product_batch_del),
    path('product_up_down',product_up_down),
    path('to_product_add',to_product_edit),
    path('uploadImages',uploadImages),
    path('product_edit',product_edit_add),
    path('to_product_edit',to_product_edit),
    path('user_list',user_list),
    path('to_user_edit',to_user_edit),
    path('user_del',user_del),
    path('user_batch_del',user_batch_del),
    path('order_list',order_list),
    path('order_batch_del',order_batch_del),
    path('comment_list',comment_list),
    path('comment_del',comment_del),
    path('to_comment_edit',to_comment_edit),
    path('comment_edit',comment_edit),
    path('charts',charts),
    path('sentiment',sentiment),
    path('cloud',cloud)
]
