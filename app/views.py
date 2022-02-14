from django.shortcuts import render,redirect
from django.urls.base import reverse
from django.contrib.auth.views import LoginView
from app.models import (Customer,Product,Cart,Order,OrderDetails)
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db.models import Max,Min,Sum
from django.views.generic.edit import CreateView,UpdateView,FormView
from app.forms import RegistrationForm,ProfileForm
from django.urls import reverse_lazy
import urllib
from app.forms import LoginForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class HomeView(View):
    def get(self,request):
        mobile=Product.objects.filter(category='M')
        laptop=Product.objects.filter(category='L')
        topWear=Product.objects.filter(category='TW')
        bottomWear=Product.objects.filter(category='BW')  
        return render(request,'app/home.html',{'mobile':mobile,'laptop':laptop,'topWear':topWear,'bottomWear':bottomWear})

class Mobile(View):
    template_name='app/mobile.html'
    def get(self,request,data=None):
        minMaxPrice=None
        price=None
        if data==None:
            mobiles=Product.objects.filter(category='M')
        elif data=='Apple' or data=='Samsung': 
            mobiles=Product.objects.filter(category='M',brand=data)
        if mobiles:
            minMaxPrice=mobiles.aggregate(Min("discounted_price"),Max("discounted_price")) 
            price=minMaxPrice.get('discounted_price__max')
        if 'price' in self.request.GET:
            price=self.request.GET['price']
            mobiles=mobiles.filter(discounted_price__lte=price)

        return render(request,self.template_name,{'mobiles':mobiles,'price':minMaxPrice,'priceValue':price})       

class ProductDetail(DetailView):
    model=Product
    template_name='app/productdetail.html'
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        if self.request.user.is_authenticated or self.request.user.is_anonymous:
            context['productAlreadyInCart']=Cart.objects.filter(user=self.request.user,product__id=self.kwargs['pk']).exists()
        return context
    
    
class Registration(CreateView):
    form_class=RegistrationForm
    template_name='app/customerregistration.html'
    success_url=reverse_lazy('login')
    def form_valid(self, form):
        super().form_valid(form)
        return redirect('/login/?' + urllib.parse.urlencode({'success':'yes'}))

class Login(LoginView):
    template_name='app/login.html'
    authentication_form=LoginForm 
    
    def form_valid(self, form):
        userName=form.cleaned_data['username']
        usering=User.objects.get(username=userName)
        findCustomerFlag=True if Customer.objects.filter(user=usering).exists() else False
        if not findCustomerFlag:
            profile=Customer.objects.create(user=usering)

        return super().form_valid(form)
 
    
class Profile(DetailView):
    model=Customer
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['User']=self.request.user
        context['active']='btn-primary'
        return context
    
    def get_template_names(self): 
        if self.kwargs['pk']==self.model.objects.get(user=self.request.user).id:
            self.template_name='app/profile.html'
        else:
            self.template_name='app/errorsPk.html'                
        return self.template_name
    
class ProfileUpdate(UpdateView):
    model=Customer
    form_class=ProfileForm

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['active']='btn-primary'
        context['data']=self.request.get_full_path()
        return context
    
    def get_success_url(self):
        context=self.get_context_data()
        if 'order' in context['data']:
            return reverse('checkout')
        else:
            id=self.model.objects.get(user=self.request.user).id
            return reverse('profile',kwargs={'pk':id})
    
    def get_template_names(self): 
        if self.kwargs['pk']==self.model.objects.get(user=self.request.user).id:
            self.template_name='app/profile_update.html'
        else:
            self.template_name='app/errorsPk.html'

        return self.template_name

@method_decorator(login_required,name='dispatch')
class addToCart(View):
    def get(self,request,productPK):
        thisProduct=Product.objects.get(id=productPK)
        findThisProduct=Cart.objects.filter(user=request.user,product__id=productPK).exists()
        print(findThisProduct)
        if findThisProduct:
            return redirect('/cart/?' + urllib.parse.urlencode({'focus':productPK}))  
        else:
            Cart.objects.create(user=request.user,product=thisProduct)
            return redirect('/cart/')       

class DeleteFromCart(View):
    def get(self,request,pk):
        findPK=Cart.objects.filter(user=request.user).filter(id=pk).exists()
        if findPK:
            Cart.objects.get(id=pk).delete()
            return redirect('/cart/')
        else:
            return render(request,'app/errorsPk.html')  

@method_decorator(login_required,name='dispatch')        
class ShowCart(ListView):
    template_name='app/show_cart.html'
    def get_queryset(self):
        queryset=Cart.objects.filter(user=self.request.user).order_by('-id')
        return queryset
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)        
        related_products=Cart.objects.filter(user=self.request.user)
        totalPriceList={x.product.id:x.product.discounted_price * x.quantity for x in related_products}
        context['totalPrice']=sum(totalPriceList.values())
        return context  

                   
class IncreaseQuantity(View):
    def get(self,request): 
        pro_id=request.GET['pro_id']
        cartObject=Cart.objects.get(user=request.user,product__id=pro_id)
        cartObject.quantity +=1
        cartObject.save()
        related_products=Cart.objects.filter(user=self.request.user)
        totalPriceList={x.product.id:x.product.discounted_price * x.quantity for x in related_products}
        totalPrice=sum(totalPriceList.values())

        totalAmount=totalPrice+70
        priceForItem=totalPriceList.get(int(pro_id))

        data={
            'totalPrice':totalPrice,
            'quantity':cartObject.quantity,
            'totalAmount':totalAmount,
            'priceForItem':priceForItem,

        }
        return JsonResponse(data)
    
class ReduceQuantity(View):
    def get(self,request): 
        pro_id=request.GET['pro_id']
        cartObject=Cart.objects.get(user=request.user,product__id=pro_id)
        cartObject.quantity -=1
        cartObject.save()
        related_products=Cart.objects.filter(user=self.request.user)
        totalPriceList={x.product.id:x.product.discounted_price * x.quantity for x in related_products}
        totalPrice=sum(totalPriceList.values())

        totalAmount=totalPrice+70
        priceForItem=totalPriceList.get(int(pro_id))

        data={
            'totalPrice':totalPrice,
            'quantity':cartObject.quantity,
            'totalAmount':totalAmount,
            'priceForItem':priceForItem,

        }
        return JsonResponse(data)
              
@method_decorator(login_required,name='dispatch') 
class Checkout(View):
    def get(self,request):
        cartData=Cart.objects.filter(user=request.user)
        totalPriceList={x.product.id:x.product.discounted_price * x.quantity for x in cartData}

        totalPrice=sum(totalPriceList.values())
        amount=cartData.aggregate(Sum('quantity'))
        return render(request, 'app/checkout.html',{
            'cartData':cartData,
            'amount':amount.get('quantity__sum'),
            'totalPrice':totalPrice
            })

class addToOrders(View):
    def get(self,request):
        cartData=Cart.objects.filter(user=request.user)
        unFinishedOrder=Order.objects.filter(user=request.user,is_finished=False).exists()
        if not unFinishedOrder:
            Order.objects.create(user=request.user)
        userOrder=Order.objects.get(user=request.user,is_finished=False)
            
        if cartData:
            for data in cartData:
                OrderDetails.objects.create(order=userOrder,product=data.product,quantity=data.quantity,
                                            total_price=data.total_price)
                data.delete()                
                
        return redirect('/orders/')
    
@method_decorator(login_required,name='dispatch')
class ShowOrders(ListView):
    template_name='app/unfinished_orders.html'
    def get_queryset(self):
        queryset=OrderDetails.objects.filter(order__user=self.request.user,order__is_finished=False)
        return queryset
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)        
        related_products=OrderDetails.objects.filter(order__user=self.request.user,order__is_finished=False)
        totalPriceList={x.product.id:x.product.discounted_price * x.quantity for x in related_products}
        context['totalPrice']=sum(totalPriceList.values())
        allQuantity=related_products.aggregate(Sum('quantity'))
        context['amount']=allQuantity.get('quantity__sum')
        if Order.objects.filter(user=self.request.user,is_finished=False).exists():
            context['unfinishedOrder']=Order.objects.get(user=self.request.user,is_finished=False)
        print(self.get_queryset)
        return context  

    


       
def UpdateProfileFromCheckout(request,pk):
    return redirect(f'/profile_update/{pk}/?' + urllib.parse.urlencode({'order':'yes'}))  

    

def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
 return render(request, 'app/address.html')



def checkout(request):
 return render(request, 'app/checkout.html')


def handle_not_found(request,exception):
    return render(request,'app/not_found.html')



