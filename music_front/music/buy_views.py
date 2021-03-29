from django.http import JsonResponse
from django.shortcuts import render,redirect

# Create your views here.
from music.models import *

import datetime
def buyproduct(request):
    uid = int(request.POST.get("uid"))
    carts = Cart.objects.filter(uid=uid)
    user = User.objects.get(u_id=uid)
    prices = 0
    for cart in carts:
        user = User.objects.get(u_id=uid)
        prices += (cart.count * int(cart.price))
    if int(user.u_balance) < prices:
        err = "余额不足，请去充值！"
        return redirect("/cart?err="+err)
    user.u_balance = str(int(user.u_balance) - prices)
    user.save()


    for cart in carts:
        order = Order()
        order.o_id = int(cart.cid)
        order.u_id = cart.uid
        order.p_id = cart.pid
        order.o_count = cart.count
        order.o_price = str(prices)
        order.o_address = cart.uid.u_address
        order.o_receiver = cart.uid.u_name
        order.o_phone = cart.uid.u_phone
        order.o_state = "1"
        order.save()

        comment = Comment()
        comment.c_id = int(cart.cid)
        comment.u_id = cart.uid
        comment.p_id = cart.pid
        comment.c_content = ""
        comment.c_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment.c_state = "1"
        comment.save()
        cart.delete()

        product = Product.objects.get(p_id=cart.pid.p_id)
        product.p_sku = str(int(product.p_sku) - int(cart.count))
        product.save()

    return redirect("/first")



# 登录
def login(request):
    username = str(request.POST.get('username'))
    password = str(request.POST.get('password'))
    result = User.objects.filter(u_login_name=username,u_login_password=password).filter(u_state="1")
    if len(result) == 0:
        return redirect("/first")
    else:
        response = redirect("/first")
        # response.set_cookie(key='username',value=username)
        response.set_cookie(key='u_id', value=result[0].u_id)
        return response

# 注销
def cancel(request):
    response = redirect('/first')
    # response.delete_cookie('username')
    response.delete_cookie('u_id')
    return response