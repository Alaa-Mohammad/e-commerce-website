from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.html import format_html

STATE_CHOICES=(
    ('North','North'),('South','South')
)

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200, null = True, blank = True)
    locality=models.CharField(max_length=200, null = True, blank = True)
    city=models.CharField(max_length=50, null = True, blank = True)
    zipcode=models.IntegerField(null = True, blank = True)
    state=models.CharField(choices=STATE_CHOICES,max_length=50, null = True, blank = True)
    
    def __str__(self):
        return str(self.id)
    
    def totalCartItem(self):
        return Cart.objects.filter(user=self.user).count()  
    

CATEGORY_CHOICES=(
    ('M','Mobile'),('L','Laptob'),('TW','Top Wear'),('BW','Bottom Wear')
)    

class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='productImg')
    
    def image_tag(self):
        return format_html(
            '<img src="/media/{}" style="width:40px;height:40px;border-radius:50%;"  />'.format(self.product_image))
    
    
    def __str__(self):
        return str(self.id)
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
 
    def __str__(self):
        return str(self.id)  
    @property 
    def total_price(self):
        return self.product.discounted_price * self.quantity 
    
       
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order_date=models.DateTimeField(default=datetime.now)
    is_finished=models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)     
    
class OrderDetails(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    total_price=models.FloatField()
    quantity=models.PositiveIntegerField()
    
    def __str__(self):
        return str(self.id)

    
    