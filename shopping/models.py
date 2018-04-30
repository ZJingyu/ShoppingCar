from django.db import models

# 用户表
class User(models.Model):
    number = models.IntegerField()               # 用户编号
    username = models.CharField(max_length=20)   # 用户名称
    password = models.CharField(max_length=20)   # 用户密码, 密码没有加密
    money = models.IntegerField()                # 账户余额

# 商品表
class Good(models.Model):
    number = models.IntegerField()               # 商品编号
    name = models.CharField(max_length=20)       # 商品名称
    price = models.CharField(max_length=20)      # 商品价格
    count = models.IntegerField()                # 商品数量


    class Meta:
        ordering = ["id"]

# 购买记录
class Record(models.Model):
    time = models.CharField(max_length=20)       # 购买时间
    amount = models.IntegerField()               # 消费金额
    goods = models.CharField(max_length=100)     # 购买商品
    number = models.IntegerField()               # 购买数量
    username = models.CharField(max_length=20)   # 用户名称

    class Meta:
        ordering = ["time"]

# 形成一个购物车，用于存放某个用户已选中但未支付的商品
class Car(models.Model):
    index = models.IntegerField()                # 加入序号
    name = models.CharField(max_length=100)      # 商品名称
    price = models.CharField(max_length=100)     # 商品总价
    count = models.IntegerField()                # 商品数量
    date = models.CharField(max_length=20)       # 加入时间
    username = models.CharField(max_length=20)   # 用户名称

    class Meta:
        ordering = ["id"]
