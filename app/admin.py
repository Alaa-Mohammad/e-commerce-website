from sre_parse import State
from django.contrib import admin
from app.models import (Customer,Product,Cart,Order,OrderDetails)
from django.utils.html import format_html

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['id','name','user','locality','city','zipcode','state','totalCartItem']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','descrip','brand','category','image_tag']
    readonly_fields=['photo_tag']

    def photo_tag(self,obj):
        return format_html(
            '<img src="/media/{}" style="width:70px;height:70px;"  />'.format(obj.product_image))   
        
    def descrip(self,obj):
        return  obj.description[:20]+'....'
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity','total_price']

@admin.register(Order)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','order_date','is_finished']
    
@admin.register(OrderDetails)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','order','product','quantity','total_price']    
