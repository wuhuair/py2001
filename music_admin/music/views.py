from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from music.models import *

# Create your views here.

def index(request):
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
        key = request.GET.get("key")     # 搜索的值
        rkey = ""
        if key == None or key == "":
            products = ProductType.objects.filter(pt_state='1')  # 0删除   1显示
        else:
            rkey = key
            products = ProductType.objects.filter(pt_state='1').filter(pt_name__icontains=rkey)
        pindex = request.GET.get("pindex")
        paginator = Paginator(products, 3)
        if pindex == None or pindex == "":
            pindex = 1
        else:
            pindex = int(pindex)
        if pindex > paginator.num_pages:
            pindex = paginator.num_pages
        page = paginator.page(pindex)
        username = User.objects.get(u_id=u_id).u_login_name
        return render(request, "product_type_list.html", {"page": page, "pindex": pindex, "key": rkey,"login_username":username})


#去编辑界面
def to_product_type_edit(request):
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
        pt_id = request.GET.get("pt_id")
        key = request.GET.get("key")
        pindex = request.GET.get("pindex")
        product_type = ProductType.objects.get(pt_id=pt_id)
        username = User.objects.get(u_id=u_id).u_login_name
        return render(request,"product_type_edit.html",{"product_type":product_type,"key":key,"pindex":pindex,"login_username":username})

#编辑后保存，回到列表页
def product_type_edit_or_add(request):
    product = ProductType()
    key = request.POST.get("key")
    pindex = request.POST.get("pindex")
    product.pt_id = request.POST.get("pt_id")
    product.pt_name = request.POST.get("pt_name")
    product.pt_state = '1'
    product.save()

    return redirect("/index?key="+key+"&pindex="+pindex)


#删除商品类型
def product_type_del(request):
    pt_id = request.GET.get("id")
    key = request.GET.get("key")
    pindex = request.GET.get("pindex")
    queryset = ProductType.objects.get(pt_id=pt_id)
    queryset.pt_state = '0'
    queryset.save()
    return redirect("/index?key="+key+"&pindex="+pindex)


#去添加页面
def to_product_type_add(request):
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
        # r = redis.Redis()
        # pt_id = r.incr("product_type_index")
        # pt_id = '20'
        queryset = ProductType.objects.last()
        pt_id = queryset.pt_id + 1
        product_type = ProductType()
        product_type.pt_id = pt_id   #/////
        key = request.GET.get("key")
        pindex = request.GET.get("pindex")
        username = User.objects.get(u_id=u_id).u_login_name
        return render(request, "product_type_edit.html", {"product_type": product_type, "key": key, "pindex": pindex,"login_username":username})