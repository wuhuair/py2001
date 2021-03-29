from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,TemplateView
from music.models import *
import redis


#查询所有订单数据，返回到前端，分页
def comment_list(request):
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
            comments = Comment.objects.filter(c_state='1')  # 0删除   1显示
        else:
            rkey = key
            comments = Comment.objects.filter(c_state='1').filter(u_id=rkey)
        pindex = request.GET.get("pindex")
        paginator = Paginator(comments, 3)
        if pindex == None or pindex == "":
            pindex = 1
        else:
            pindex = int(pindex)
        if pindex > paginator.num_pages:
            pindex = paginator.num_pages
        page = paginator.page(pindex)
        # private_commentlist = Comment.objects.filter(c_state='1').filter(u_id_id=u_id)
        # for private_comment in private_commentlist:
        #     private_comment.u_id_id = User.objects.get(u_id=u_id).u_login_name
        #     private_comment,
        username = User.objects.get(u_id=u_id).u_login_name
        return render(request,"comment_list.html",{"page":page,"pindex":pindex,"key":rkey,"login_username":username,"u_id":int(u_id)})

#删除评论
def comment_del(request):
    c_id = request.GET.get("id")
    key = request.GET.get("key")
    pindex = request.GET.get("pindex")
    comment = Comment.objects.get(c_id=c_id)
    comment.c_state = '0'
    comment.save()
    return redirect("/comment_list?key=" + key + "&pindex=" + pindex)


#去编辑
def to_comment_edit(request):
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
        pindex = request.GET.get("pindex")
        key = request.GET.get("key")
        c_id = request.GET.get("c_id")
        comment = Comment.objects.get(c_id=c_id)
        login_name = comment.u_id.u_login_name
        product_name = comment.p_id.p_name
        username = User.objects.get(u_id=u_id).u_login_name
        return render(request, "comment_edit.html", {"comment":comment,"login_name": login_name, "pindex": pindex, "key": key,"product_name":product_name,"login_username":username})



#商品编辑
def comment_edit(request):
    comment = Comment()
    c_id = request.POST.get("c_id")
    comment.c_id = c_id
    u_id = request.POST.get("u_id")
    comment.u_id = User.objects.get(u_id=u_id)
    p_id = request.POST.get("p_id")
    comment.p_id = Product.objects.get(p_id=p_id)
    comment.c_content = request.POST.get("c_content")
    comment.c_time = request.POST.get("c_time")
    comment.c_state = "1"
    comment.save()
    return redirect("/comment_list")