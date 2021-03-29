from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from music.models import *
import requests


# Create your views here.

# 登录
def into_login(request):
    response = render(request,'login.html')
    # response.delete_cookie('username')
    response.delete_cookie('u_id')
    return response


def login(request):
    username = str(request.POST.get('username'))
    password = str(request.POST.get('password'))
    result = User.objects.filter(u_login_name=username,u_login_password=password).filter(u_state="1")
    if len(result) == 0:
        return render(request,"login.html",{'err':'用户名或密码错误!'})
    else:
        response = redirect("/index")
        # response.set_cookie(key='username',value=username)
        response.set_cookie(key='u_id', value=result[0].u_id)
        return response
        # return redirect("/index?username="+username+"&password="+password+"&u_id="+u_id)


# 注册
def register(request):
    response = render(request,'register.html')
    # response.delete_cookie('username')
    response.delete_cookie('u_id')
    return response


def success(request):
    u_pay_password = request.POST.get('u_pay_password')
    re_u_pay_password = request.POST.get('re_u_pay_password')
    u_login_password = request.POST.get('u_login_password')
    re_u_login_password = request.POST.get('re_u_login_password')
    u_login_name = request.POST.get('u_login_name')

    u_id = request.POST.get("u_id")
    user = User()
    if u_id == None or u_id == "":
        last_data = User.objects.last()
        user.u_id = last_data.u_id + 1  # 新id
    else:
        user.u_id = u_id
    if len(User.objects.filter(u_login_name=u_login_name,u_state='1')) != 0:
        return render(request,"register.html",{'err':'用户名已存在'})
    elif u_pay_password != re_u_pay_password and u_login_password != re_u_login_password:
        return render(request,"register.html",{'err':'两次输入密码不相同'})
    else:
        user.u_name = request.POST.get('u_name')
        user.u_phone = request.POST.get('u_phone')
        user.u_email = request.POST.get('u_email')
        user.u_address = request.POST.get('u_address')
        user.u_login_name = request.POST.get('u_login_name')
        user.u_login_password = u_login_password
        user.u_pay_password = u_pay_password
        user.u_balance = 9999
        user.u_state = "1"
        user.save()
        return render(request,"login.html")



# 查询用户
def user_list(request):
    try:                                 # 验证登录，没登录无法进入系统
        # username = request.COOKIES['username']
        u_id = request.COOKIES['u_id']
    except:
        return redirect("/to_login")
    else:
        result = False
        # username = request.COOKIES['username']
        u_id = request.COOKIES['u_id']
        if u_id != None or u_id != "":
            result = True
        else:
            return redirect("/to_login")

    if result:
        key = request.GET.get("key")
        rkey = ""
        if key == None or key == "":
            users = User.objects.filter(u_state='1')  # 0删除   1显示
        else:
            rkey = key
            users = User.objects.filter(u_state='1').filter(u_name__icontains=rkey)
        pindex = request.GET.get("pindex")
        paginator = Paginator(users, 3)
        if pindex == None or pindex == "":
            pindex = 1
        else:
            pindex = int(pindex)
        if pindex > paginator.num_pages:
            pindex = paginator.num_pages
        page = paginator.page(pindex)
        username = User.objects.get(u_id=u_id).u_login_name
        return render(request, "user_list.html", {"page": page, "pindex": pindex, "key": rkey,"login_username":username})

# 去编辑
def to_user_edit(request):
    key = request.GET.get('key')
    pindex = request.GET.get('pindex')
    u_id = request.GET.get('u_id')
    user = User.objects.get(u_id=u_id)
    return render(request,"register.html",{"user":user,"key":key,"pindex":pindex})

#删除用户
def user_del(request):
    u_id = request.GET.get("id")
    key = request.GET.get("key")
    pindex = request.GET.get("pindex")
    user = User.objects.get(u_id=u_id)
    user.u_state = '0'
    user.save()
    return redirect("/user_list?key=" + key + "&pindex=" + pindex)

#批量删除
def user_batch_del(request):
    ids_ = request.GET.get("ids")
    key = request.GET.get("key")
    pindex = request.GET.get("pindex")
    ids = ids_.rstrip("-").split("-")
    for id in ids:
        user = User.objects.get(u_id=id)
        user.u_state = '0'
        user.save()
    return redirect("/user_list?key=" + key + "&pindex=" + pindex)