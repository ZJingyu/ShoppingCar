from django.contrib import admin
from . models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "username", "money")

@admin.register(Good)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "name", "price", "count")
    search_fields = ("number", "name")

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("id", "time", "amount", "number", "goods", "username")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("id", "index", "name", "price", "count", "date", "username")

admin.site.site_header = "购物车后台管理界面"


