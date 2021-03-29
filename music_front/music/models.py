from django.db import models

# Create your models here.

#耳机商品类型表
class ProductType(models.Model):
    pt_id = models.IntegerField(primary_key=True,verbose_name='耳机类型编号')   #商品类型编号
    pt_name = models.CharField(max_length=200,verbose_name='耳机类型名称')    #商品类型名称
    pt_state = models.CharField(max_length=2)    #默认不删除

#商品售卖类型
class SaleProductType(models.Model):
    spt_id = models.IntegerField(primary_key=True,verbose_name='耳机售卖类型编号')    #商品售卖类型编号
    spt_name = models.CharField(max_length=200,verbose_name='耳机售卖类型名称')        #商品售卖类型名称
    spt_use = models.CharField(max_length=255,verbose_name='使用方式')         #使用方式
    spt_jack = models.CharField(max_length=255,verbose_name='插口类型')        #插口类型
    spt_brand = models.CharField(max_length=255,verbose_name='品牌')       #品牌
    spt_length = models.CharField(max_length=255,verbose_name='线长')      #线长

#商品表
class Product(models.Model):
    p_id = models.IntegerField(primary_key=True,verbose_name='商品编号')      # 商品编号，主键
    p_imgs = models.CharField(max_length=255,verbose_name='图片')         # 图片
    p_name = models.CharField(max_length=200,verbose_name='商品名称')         # 商品名称
    p_cost_price = models.FloatField(max_length=10,verbose_name='商品成本价格')   # 商品成本价格
    p_sale_prict = models.FloatField(max_length=10,verbose_name='商品售卖价格')   # 商品售卖价格
    p_postage = models.IntegerField(max_length=10,verbose_name='邮费')    # 邮费
    p_sku = models.IntegerField(max_length=20,verbose_name='库存')        # 库存
    p_size = models.CharField(max_length=200,verbose_name='商品尺寸')         # 商品尺寸
    # p_weight = models.FloatField(max_length=10,verbose_name='商品重量')       # 商品重量
    p_hot = models.CharField(max_length=2,verbose_name='是否热卖')            # 热卖
    p_recommend = models.CharField(max_length=2,verbose_name='是否推荐')      # 推荐
    p_state = models.CharField(max_length=2,verbose_name='状态')          # 状态
    pt_id = models.ForeignKey(ProductType, on_delete=models.CASCADE,verbose_name='类型')  # 类型
    # p_up_down = models.IntegerField(choices=[(0,'下架'),(1,'上架')],default=1,verbose_name='上/下架')      # 上/下架
    p_up_down = models.CharField(max_length=2, verbose_name='上/下架')  # 状态

#商品售卖类型和商品表中间表
class Middle(models.Model):
    m_id = models.IntegerField(primary_key=True,verbose_name='中间表编号')  #编号
    spt_id = models.ForeignKey(SaleProductType,on_delete=models.CASCADE,verbose_name='售卖类型编号')
    p_id = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='商品编号')
    m_use = models.CharField(max_length=255,verbose_name='使用方式')    #使用方式


class User(models.Model):
    u_id = models.IntegerField(primary_key=True,verbose_name='用户编号')   #用户编号
    u_name = models.CharField(max_length=20,verbose_name='名字')    #名字
    u_phone = models.CharField(max_length=30,verbose_name='电话')   #电话
    u_email = models.CharField(max_length=50,verbose_name='邮箱')  #邮箱
    u_address = models.CharField(max_length=200,verbose_name='地址')  #地址
    u_login_name = models.CharField(max_length=20,verbose_name='登录名') #登录名
    u_login_password = models.CharField(max_length=100,verbose_name='登录密码')  #登录密码
    u_balance = models.CharField(max_length=20,verbose_name='账户余额')  # 账户余额
    u_pay_password = models.CharField(max_length=100,verbose_name='支付密码')  # 支付密码
    # u_state = models.IntegerField(choices=[(0,'锁定'),(1,'正常')],default=1,verbose_name='状态')   #状态
    u_state = models.CharField(max_length=2, verbose_name='状态')  # 状态

class Order(models.Model):
    o_id = models.IntegerField(primary_key=True,verbose_name='订单编号')    #订单编号
    u_id = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='关联用户')  #关联用户   购买用户名
    p_id = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='关联商品')   #关联商品   购买商品名
    o_count = models.IntegerField(max_length=10,verbose_name='购买数量')       #购买数量
    o_price = models.FloatField(max_length=20,verbose_name='购买价格')        #购买价格
    # o_postal_code = models.IntegerField(max_length=20,verbose_name='邮编')  #邮编
    o_address = models.CharField(max_length=50,verbose_name='邮购地址')     #邮购地址
    o_receiver = models.CharField(max_length=50,verbose_name='收货人')   #收货人
    o_phone = models.CharField(max_length=50,verbose_name='电话')    #电话
    # o_state = models.IntegerField(choices=[(0,'删除'),(1,'显示'),],default=1,verbose_name='状态')     #状态
    o_state = models.CharField(max_length=2,verbose_name='状态')  # 状态

class Comment(models.Model):
    c_id = models.IntegerField(primary_key=True,verbose_name='评论id')   #评论id
    u_id = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='关联用户')   #关联用户
    p_id = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='关联商品')  #关联商品
    # o_id = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='关联订单')  # 关联商品
    c_content = models.CharField(max_length=200,verbose_name='评论内容',blank=True)   #评论内容
    c_time = models.DateTimeField(auto_now_add=True)        #评论时间
    # c_state = models.IntegerField(choices=[(0,'删除'),(1,'显示'),],default=1,verbose_name='状态')  #状态
    c_state = models.CharField(max_length=2,verbose_name='状态')  # 状态

#图片上传地址
class ProductImage(models.Model):
    img = models.ImageField(upload_to='product_imgs',null=True)


class Cart(models.Model):
    cid = models.CharField(max_length=255,primary_key=True,verbose_name='购物车id')
    pid = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='关联商品')
    uid = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='关联用户')
    price = models.FloatField(max_length=20, verbose_name='购买价格')
    count = models.IntegerField(max_length=10, verbose_name='购买数量')