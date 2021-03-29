from django.http import JsonResponse
from django.shortcuts import render,redirect

# Create your views here.
from music.models import *


def index(request):
    try:                         # 验证登录，没登录无法进入系统
        u_id = request.COOKIES['u_id']
    except:
        u_id = None
        username = None
    else:
        u_id = request.COOKIES['u_id']
        username = User.objects.get(u_id=u_id).u_login_name
    products = SaleProductType.objects.all()
    for product in products:
        product.spt_use = product.spt_use.split(',')
        product.spt_jack = product.spt_jack.split(',')
        product.spt_brand = product.spt_brand.split(',')
        product.spt_length = product.spt_length.split(',')
    hot_products = Product.objects.filter(p_state='1').filter(p_hot='是')
    for hot in hot_products:
        hot.p_imgs = hot.p_imgs.split(",")[0]
    return render(request,'index.html',{"products":products,"hot_products":hot_products[3:8],"hot_0":hot_products[0],"hot_1":hot_products[1],"hot_2":hot_products[2],"username":username,"u_id":u_id})


def products(request):
    try:                         # 验证登录，没登录无法进入系统
        u_id = request.COOKIES['u_id']
    except:
        u_id = None
        username = None
    else:
        u_id = request.COOKIES['u_id']
        username = User.objects.get(u_id=u_id).u_login_name
    products = SaleProductType.objects.all()
    for product in products:
        product.spt_use = product.spt_use.split(',')
        product.spt_jack = product.spt_jack.split(',')
        product.spt_brand = product.spt_brand.split(',')
        product.spt_length = product.spt_length.split(',')

    spt_id = request.GET.get("spt_id")
    use = request.GET.get("use")
    jack = request.GET.get("jack")
    brand = request.GET.get("brand")
    length = request.GET.get("length")
    arr = [use,jack,brand,length]
    m_use = list(filter(lambda x:x!="" and x!=None,arr))[0]
    middles = Middle.objects.filter(spt_id=spt_id).filter(m_use=m_use)[0:3 ]
    for middle in middles:
        middle.p_id.p_imgs = middle.p_id.p_imgs.split(",")[0]
    if len(middles) == 3:
        loadmore = "加载更多..."
    else:
        loadmore = "已加载全部"

    return render(request,"products.html",{"products":products,"middles":middles,"loadmore":loadmore,"spt_id":spt_id,"m_use":m_use,"username":username,"u_id":u_id})

def products_ajax(request):
    page = int(request.GET.get("page"))
    spt_id = request.GET.get("spt_id")
    m_use = request.GET.get("m_use")
    middles = Middle.objects.filter(spt_id=spt_id).filter(m_use=m_use)[(page-1)*3:page*3]
    for middle in middles:
        middle.p_id.p_imgs = middle.p_id.p_imgs.split(",")[0]
    dict = {}
    product_items = []
    for middle in middles:
        product_item = {}
        product_item["p_id"] = middle.p_id.p_id
        product_item["p_imgs"] = middle.p_id.p_imgs
        product_item["p_name"] = middle.p_id.p_name
        product_item["p_sale_prict"] = middle.p_id.p_sale_prict
        product_items.append(product_item)
    dict["product_items"] = product_items
    dict["spt_id"] = spt_id
    dict["m_use"] = m_use
    if len(middles) == 3:
        loadmore = "加载更多..."
    else:
        loadmore = "已加载全部"
    dict["loadmore"] = loadmore
    return JsonResponse(dict)


def FindProductsByPrict(request):
    prict1 = request.GET.get("prict1")
    prict2 = request.GET.get("prict2")
    spt_id = request.GET.get("spt_id")
    m_use = request.GET.get("m_use")
    middles = Middle.objects.filter(spt_id=spt_id).filter(m_use=m_use)
    dict = {}
    product_items = []
    for middle in middles:
        middle.p_id.p_imgs = middle.p_id.p_imgs.split(",")[0]
        if (middle.p_id.p_sale_prict <= int(prict1)) or (middle.p_id.p_sale_prict > int(prict2)):
            continue
        product_item = {}
        product_item["p_id"] = middle.p_id.p_id
        product_item["p_imgs"] = middle.p_id.p_imgs
        product_item["p_name"] = middle.p_id.p_name
        product_item["p_sale_prict"] = middle.p_id.p_sale_prict
        product_items.append(product_item)
    dict["product_items"] = product_items
    dict["spt_id"] = spt_id
    dict["m_use"] = m_use
    return JsonResponse(dict)

def single(request):
    try:  # 验证登录，没登录无法进入系统
        u_id = request.COOKIES['u_id']
    except:
        u_id = None
        username = None
    else:
        u_id = request.COOKIES['u_id']
        username = User.objects.get(u_id=u_id).u_login_name
    id = request.GET.get("id")
    product_view = Product.objects.get(p_id=id)
    product_view.p_imgs = product_view.p_imgs.split(",")
    products = SaleProductType.objects.all()
    comments = Comment.objects.filter(p_id=id)
    for product in products:
        product.spt_use = product.spt_use.split(',')
        product.spt_jack = product.spt_jack.split(',')
        product.spt_brand = product.spt_brand.split(',')
        product.spt_length = product.spt_length.split(',')
    return render(request, 'single.html',{"products": products,"product_view":product_view,"comments":comments,"username":username,"u_id":int(u_id)})

import time
def addcart(request):
    try:                                 # 验证登录，没登录无法进入系统
        u_id = request.COOKIES['u_id']
    except:
        return redirect("/first")
    else:
        result = False
        u_id = request.COOKIES['u_id']
        if u_id != None or u_id != "":
            result = True
        else:
            return redirect("/first")

    if result:
        cart = Cart()
        cart.cid = int(time.time())
        cart.uid = User.objects.get(u_id=int(u_id))
        cart.pid = Product.objects.get(p_id=int(request.GET.get("pid")))
        cart.count = int(request.GET.get("count"))
        cart.price = float(request.GET.get("prict"))
        cart.save()
        return redirect("/cart")



def cart(request):
    try:  # 验证登录，没登录无法进入系统
        u_id = request.COOKIES['u_id']
    except:
        return redirect("/first")
    else:
        result = False
        u_id = request.COOKIES['u_id']
        if u_id != None or u_id != "":
            result = True
        else:
            return redirect("/first")

    if result:
        products = SaleProductType.objects.all()
        err = request.GET.get("err")
        for product in products:
            product.spt_use = product.spt_use.split(',')
            product.spt_jack = product.spt_jack.split(',')
            product.spt_brand = product.spt_brand.split(',')
            product.spt_length = product.spt_length.split(',')
        uid = int(u_id)
        carts = Cart.objects.filter(uid=uid)
        for c in carts:
            c.pid.p_imgs = c.pid.p_imgs.split(",")[0]
        if err == None or err == "":
            err = ""
        username = User.objects.get(u_id=u_id).u_login_name
        return render(request, "cart.html", {"products": products, "carts": carts,"uid":uid,"err":err,"username":username,"u_id":u_id})

def delcart(request):
    cid = request.GET.get("cid")
    cart = Cart.objects.get(cid=cid)
    cart.delete()
    return redirect("/cart")

# 添加评论
def addcomment(request):
    content = request.POST.get("content")
    c_id = request.POST.get("c_id")
    comment = Comment.objects.get(c_id=c_id)
    comment.c_content = content
    comment.save()
    id = str(comment.p_id.p_id)
    return redirect("/single?id="+id)
