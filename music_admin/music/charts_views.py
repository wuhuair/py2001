from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from music.models import *
import time
from wordcloud import WordCloud
import jieba
import matplotlib.pyplot as plt
from snownlp import SnowNLP

# Create your views here.

def charts(request):
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
        product_types = ProductType.objects.all().filter(pt_state='1')
        pt_names = []
        pt_nums = []
        for product_type in product_types:
            pt_name = product_type.pt_name
            pt_names.append(pt_name)
            pt_num = len(Product.objects.filter(pt_id=product_type.pt_id))
            pt_nums.append(pt_num)
        products = Product.objects.all()
        a,b,c,d,e = 0,0,0,0,0
        i = 0
        for product in products:
            i += 1
            if int(product.p_sale_prict) >= 0 and int(product.p_sale_prict) < 100:
                a += 1
            if int(product.p_sale_prict) >= 100 and int(product.p_sale_prict) < 300:
                b += 1
            if int(product.p_sale_prict) >= 300 and int(product.p_sale_prict) < 600:
                c += 1
            if int(product.p_sale_prict) >= 600 and int(product.p_sale_prict) < 1000:
                d += 1
            if int(product.p_sale_prict) >= 1000:
                e += 1
        a = round(a/i*100,2)
        b = round(b/i*100,2)
        c = round(c/i*100,2)
        d = round(d/i*100,2)
        e = round(e/i*100,2)
        if a+b+c+d+e < 100:
            a += 100 - a+b+c+d+e
        elif a+b+c+d+e > 100:
            a -= a+b+c+d+e - 100
        lis = [['0-100元',a],['100-300元',b],['300-600元',c],['600-1000元',d],['1000元以上',e]]

        orders = Order.objects.filter(u_id=u_id)
        money = 0
        Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec = 0,0,0,0,0,0,0,0,0,0,0,0     #初始化每个月消费额为0
        for order in orders:
            timeStamp = int(order.o_id)            # 将时间戳转为时间格式
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%m", timeArray)
            if int(otherStyleTime) == 1:            # 若果等于1，就代表是一月消费的订单
                Jan += int(order.o_price)             # 计算消费额
            if int(otherStyleTime) == 2:
                Feb += int(order.o_price)
            if int(otherStyleTime) == 3:
                Mar += int(order.o_price)
            if int(otherStyleTime) == 4:
                Apr += int(order.o_price)
            if int(otherStyleTime) == 5:
                May += int(order.o_price)
            if int(otherStyleTime) == 6:
                Jun += int(order.o_price)
            if int(otherStyleTime) == 7:
                Jul += int(order.o_price)
            if int(otherStyleTime) == 8:
                Aug += int(order.o_price)
            if int(otherStyleTime) == 9:
                Sep += int(order.o_price)
            if int(otherStyleTime) == 10:
                Oct += int(order.o_price)
            if int(otherStyleTime) == 11:
                Nov += int(order.o_price)
            if int(otherStyleTime) == 12:
                Dec += int(order.o_price)
        datas = [Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec]
        # print(datas)
        username = User.objects.get(u_id=u_id).u_login_name
        return render(request, "bar-charts.html", {'pt_names': pt_names, 'pt_nums': pt_nums,"lis":lis,"login_username":username,"u_id":int(u_id),"datas":datas,"a":a,"b":b,"c":c,"d":d,"e":e})



def sentiment(request):
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
        products = Product.objects.all()
        username = User.objects.get(u_id=u_id).u_login_name
        return render(request,"cloud_sentiment.html",{"products":products,"login_username":username})

def cloud(request):
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
        p_id = request.GET.get("p_id")
        comments = Comment.objects.filter(p_id=p_id)
        str_comment = ""
        x, y, z,s = 0, 0, 0,0  # 好 中 差 总
        for comment in comments:
            str_comment += comment.c_content
            if len(comment.c_content) != 0:
                s += 1
                score = SnowNLP(comment.c_content)
                score_new = score.sentiments
                if score_new > 0.6:
                    x += 1
                elif 0.6 >= score_new > 0.4:
                    y += 1
                else:
                    z += 1
        jieba_list = jieba.cut(str_comment, cut_all=True)   # 是列表形式
        jieba_str = " ".join(jieba_list)
        wordclod_my = WordCloud(font_path='E:\PycharmProjects\music_admin\music\simhei.ttf').generate(jieba_str)
        plt.imshow(wordclod_my)
        plt.axis("off")
        plt.savefig("E:\PycharmProjects\music_admin\static\cloud\{0}.jpg".format(p_id))
        plt.close()
        username = User.objects.get(u_id=u_id).u_login_name
        return render(request,"cloud_sentiment.html",{"p_id":p_id,"login_username":username,"x":x,"y":y,"z":z,"s":s})
