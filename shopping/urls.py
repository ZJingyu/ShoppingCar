from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('shopping/', views.shopping, name="shopping"),

    # 隐藏的购物车查询url
    path('shopping_car_history/', views.shopping_car_history, name="shopping_car_history"),
    path('user_register/', views.register, name="register"),
    path('shopping_purchase/', views.shopping_purchase, name="shopping_purchase"),

    # 隐藏的购物车数据添加
    path('shopping_car/', views.shopping_car,),

    path('consume/', views.consume, name="consume"),
    path('recharge/', views.recharge, name="recharge"),  # 用户充值
    path("recharge_confirm/", views.recharge_confirm, name="confirm"),
    # 登出时，清除缓存
    path("logout/", views.logout, name="logout"),

    # 注册信息填写页面
    path("register/", views.register, name="register"),
    # 注册成功的处理页
    path("register_success/", views.register_success, name="register_success"),
]
