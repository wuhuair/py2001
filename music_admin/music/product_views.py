from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,TemplateView
from music.models import *



#查询所有商品数据，返回到前端，分页
def product_list(request):
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
            products = Product.objects.filter(p_state='1')  # 0删除   1显示
        else:
            rkey = key
            products = Product.objects.filter(p_state='1').filter(p_name__icontains=rkey)
        for product in products:
            product.p_imgs = product.p_imgs.split(",")[0]
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
        return render(request,"product_list.html",{"page":page,"pindex":pindex,"key":rkey,"login_username":username})

#删除商品
def product_del(request):
    p_id = request.GET.get("id")
    key = request.GET.get("key")
    pindex = request.GET.get("pindex")
    product = Product.objects.get(p_id=p_id)
    product.p_state = '0'
    product.save()
    return redirect("/product_list?key=" + key + "&pindex=" + pindex)

#批量删除
def product_batch_del(request):
    ids_ = request.GET.get("ids")
    key = request.GET.get("key")
    pindex = request.GET.get("pindex")
    ids = ids_.rstrip("-").split("-")
    for id in ids:
        product = Product.objects.get(p_id=id)
        product.p_state = '0'
        product.save()
    return redirect("/product_list?key=" + key + "&pindex=" + pindex)

#批量上/下架
def product_up_down(request):
    ids_ = request.GET.get("ids")
    key = request.GET.get("key")
    pindex = request.GET.get("pindex")
    state = request.GET.get("state")
    ids = ids_.rstrip("-").split("-")
    for id in ids:
        product = Product.objects.get(p_id=id)
        product.p_up_down = state
        product.save()
    return redirect("/product_list?key=" + key + "&pindex=" + pindex)

#去添加
def to_product_add(request):
    # r = redis.Redis()
    # p_id = r.incr("product_type_index")
    # p_id = '50'
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
        queryset = Product.objects.last()
        p_id = queryset.p_id + 1
        pindex = request.GET.get("pindex")
        key = request.GET.get("key")
        product = Product()
        product.p_id = p_id
        product_types = ProductType.objects.all()
        username = User.objects.get(u_id=u_id).u_login_name
        return render(request,"product_edit.html",{"product":product,"product_types":product_types,"pindex":pindex,"key":key,"login_username":username})

#去编辑
def to_product_edit(request):
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
        p_id = request.GET.get("p_id")
        if p_id == "" or p_id == None:
            product_types = ProductType.objects.all()
            username = User.objects.get(u_id=u_id).u_login_name
            return render(request, "product_edit.html", {"product_types": product_types, "pindex": pindex, "key": key,"login_username":username})
        else:
            product_types = ProductType.objects.all()
            product = Product.objects.get(p_id=p_id)
            imgs = product.p_imgs.split(",")
            product.p_imgs = product.p_imgs + ','
            username = User.objects.get(u_id=u_id).u_login_name
            return render(request, "product_edit.html", {"product":product,"product_types": product_types, "pindex": pindex, "key": key,"imgs":imgs,"login_username":username})
#添加图片
def uploadImages(request):
    files = request.FILES.getlist("file")
    products = {}
    list = []
    for file in files:
        product = ProductImage.objects.create(
            img=file
        )
        list.append(product.img.url)
    products["urls"] = list
    return JsonResponse(products)

#商品编辑和添加
def product_edit_add(request):
    # r = redis.Redis()
    product = Product()
    p_id = request.POST.get("p_id")
    if p_id == "" or p_id == None:
        queryset = Product.objects.last()
        p_id = queryset.p_id + 1
        product.p_id = p_id
    else:
        product.p_id = p_id
    product.p_imgs = request.POST.get("p_imgs").rstrip(",")
    product.p_name = request.POST.get("p_name")
    product.p_cost_price = request.POST.get("p_cost_price")
    product.p_sale_prict = request.POST.get("p_sale_prict")
    product.p_postage = request.POST.get("p_postage")
    product.p_sku = request.POST.get("p_sku")
    product.p_size = request.POST.get("p_size")
    product.p_hot = request.POST.get("p_hot")
    product.p_recommend = request.POST.get("p_recommend")
    product.p_state = "1"
    pt_id = request.POST.get("p_product_type")
    product.pt_id = ProductType.objects.get(pt_id=pt_id)
    product.p_up_down = "上架"
    product.save()
    return redirect("/product_list")