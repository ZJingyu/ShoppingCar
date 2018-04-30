# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse, redirect
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json, time, random


# 用户登录和注册界面
def login(request):
    """在login这个url完成get和post请求，并在post成功时返回一个html文件，这个html可以被另外一个url以get方式访问"""
    if request.method == "GET":
        return render(request, "shopping/login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.get(username=username).password == password:
            # 缓存该用户
            request.session["user"] = {"username": username, "password": password}
            # return render(request, "shopping/shopping.html", {"goods": goods, "user": username})
            return redirect("/shopping/shopping/")  # 直接重定向到shopping页面
        else:
            return redirect("/shopping/login/")
    return redirect("/shopping/login/")

# 隐藏功能函数
def shopping_car_history(request):
    # 查询当前用户的购物车历史并计算数量返给前段显示
    car_count = len(Car.objects.filter(username=request.session["user"]["username"]))
    # print(car_count)
    return HttpResponse(json.dumps(car_count))

# shopping界面
def shopping(request):
    # 从数据库中查询相应的商品信息并传递到页面进行展示
    goods = [model_to_dict(Good.objects.get(name=x)) for _, x in enumerate(["电脑", "鼠标", "美女", "游艇"])]
    # 如果用户未登录，传给前端一个空的用户名;否则就把当前用户名传过去
    if "user" not in request.session.keys():
        request.session["user"] = " "
    return render(request, "shopping/shopping.html", {"goods": goods, "user": json.dumps(request.session["user"])})


# 用户注册信息界面
def register(request):
    return render(request, "shopping/register.html")


# 在这一步，已经使所有的用户全部登录了，那么把用户的购物车追加到Car表里
# 在把购物车历史已有的商品记录给到页面时，是没有缓存的；因此如果页面有缓存的新的商品，就可以直接追加到用户的购物车里，并清除缓存
def shopping_car(request):
    # 购物车里新增添的未支付商品
    car_new_goods = request.POST.get("car").split(",")
    # print(car_new_goods)
    if len(car_new_goods) >= 2:
        car_new_goods = car_new_goods[1:]
        car_new_good_name_count = [good.split("-") for good in car_new_goods]
        # 形成一条购物车记录:序号、商品名称、购买数量、商品总价、加入时间、当前用户
        car_records = [
            {
                "index": index,
                "name": Good.objects.get(name=value[0]).name,
                "count": value[1],
                "price": int(Good.objects.get(name=value[0]).price) * int(value[1]),
                "date": time.strftime("%Y-%m-%d %X", time.localtime()),
                "username": request.session["user"]["username"]
            } for index, value in enumerate(car_new_good_name_count)
        ]
        # 把这条记录添加到购物车那张表里
        for record in car_records:
            obj = Car.objects.create(**record)
            obj.save()
    else:
        pass
    return HttpResponse(json.dumps("ok"))


# 把用户购物车里的数据[包括ajax提交的新数据]全拿出来，放到页面去展示
def shopping_purchase(request):
    # 如果用户未登录，直接重定向到shopping页面
    if request.session["user"]:
        car = Car.objects.filter(username=request.session["user"]["username"])
        car = [model_to_dict(query) for query in car]
        return render(request, "shopping/shopping_car.html", {"car": car})
    else:
        return redirect("/shopping/shopping/")



# 做三件事：清除当前id的记录，添加消费记录，扣除金额
@csrf_exempt
def consume(request):
    # id_list = request.POST.get("id")  # 不知道为什么，这个id无法获取，这个需要请教老师
    # 现在从body里取出id
    body = request.body.decode("utf-8")  # 转码
    # 解析这种格式的字节流b'id%5B%5D=1&id%5B%5D=2&price=77994'
    body = body.split("&")[:-1]  # 切分参数，并取出id，最后一个是price
    id_list = [x.split("=")[-1] for x in body]  # 从每个key乱码=value中取出value
    price = request.POST.get("price")
    # print(id_list, type(id_list), price, type(price))
    ID = User.objects.get(username=request.session["user"]["username"])
    if ID.money < int(price):
        # 金额不足
        return HttpResponse(json.dumps(0))
    else:
        # id是唯一的，id是唯一主键的列表
        for i in id_list:
            # 获取当前id的物品的购物车信息
            car = Car.objects.get(id=i)
            # 修改字段，扣除金额
            usr = User.objects.get(username=car.username)
            usr.money = usr.money - float(car.price)  # 减去当前购物车商品的金额而不是总金额
            usr.save()
            # 添加消费记录
            record = {
                "time": time.strftime("%Y-%m-%d %X", time.localtime()),
                "amount": float(car.price) * car.count,
                "number": car.count,
                "goods": car.name,
                "username": car.username
            }
            rec = Record.objects.create(**record)
            rec.save()
            # 删除购物车信息
            car.delete()
        return HttpResponse(json.dumps(1))

# 定义充值页面
@csrf_exempt
def recharge(request):
    # 如果是get请求，是从余额不足跳转过来的
    if request.method == "GET":
        if request.session["user"]:
            return render(request, "shopping/recharge.html")
        else:
            return redirect("/shopping/login/")
    # 如果是post请求，是当前页面提交form表单的
    elif request.method == "POST":
        # post肯定是已经登录了
        money = request.POST.get("money")
        usr = User.objects.get(username=request.session["user"]["username"])
        usr.money = usr.money + float(money)
        usr.save()
        # 跳转到支付页面
        return redirect("/shopping/shopping_purchase/")

def recharge_confirm(request):
    password = request.POST.get("password")
    usr = User.objects.get(username=request.session["user"]["username"])
    # 从用户表里拉出来该用户的信息，把钱加上去
    if password == usr.password:
        return HttpResponse(1)
    else:
        return HttpResponse(0)


def logout(request):
    del request.session["user"]
    return HttpResponse(1)

# 最后一个函数，注册界面
def register(request):
    # 注册前对用户进行查询，为了对用户名是否存在进行验证
    if request.method == "GET":
        return render(request, "shopping/register.html")
    elif request.method == "POST":
        user = request.POST.get("user", "")
        if user in [user.username for user in User.objects.all()]:
            return HttpResponse("0")
        else:
            return HttpResponse("1")
    return redirect("/shopping/login/")

# 注册信息正确时，加入user表并返回登录页
def register_success(request):
    if request.method == "POST":
        dic = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
            "number": random.randint(1, 100), "money": 0}
        # 注册用户
        usr = User.objects.create(**dic)
        usr.save()
        return redirect("/shopping/login/")
    else:
        return redirect("/shopping/login/")

