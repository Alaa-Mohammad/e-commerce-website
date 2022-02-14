from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from app.forms import PasswordChangeForm,PasswordResetForm,SetPassword_Form
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.HomeView.as_view(),name='home'),
    path('product-detail/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('cart/', views.ShowCart.as_view(), name='cart'),
    path('add/<int:productPK>/',views.addToCart.as_view(),name='add_to_cart'),
    path('del/<int:pk>/', views.DeleteFromCart.as_view(), name='delete-from-cart'),
    path('increase_quantity/',views.IncreaseQuantity.as_view()),
    path('reduce_quantity/',views.ReduceQuantity.as_view()),
    
    path('profile/<int:pk>/', login_required(views.Profile.as_view(),login_url='login'), name='profile'),
    path('profile_update/<int:pk>/',login_required(views.ProfileUpdate.as_view(),login_url='login'),name='profile_update'),

    path('mobile/', views.Mobile.as_view(), name='mobile'),
    path('mobile/<slug:data>', views.Mobile.as_view(), name='mobileData'),
    path('registration/', views.Registration.as_view(), name='customerregistration'),
    path('login/', views.Login.as_view(),
         name='login'),
        path('accounts/login/', views.Login.as_view(),
         name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('password_change/',auth_views.PasswordChangeView.as_view(
      template_name="app/password_change.html",form_class=PasswordChangeForm,success_url=reverse_lazy('logout')),
         name='password_change'),
    path('password_reset/',auth_views.PasswordResetView.as_view(
      template_name='app/password_reset.html',form_class=PasswordResetForm),
         name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(
      template_name='app/password_reset_done.html'),
         name='password_reset_done'),    
    path('password_reset_confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(
      template_name='app/password_reset_confirm.html',form_class=SetPassword_Form,success_url=reverse_lazy('logout')),
         name='password_reset_confirm'),       
  
    path('checkout/', views.Checkout.as_view(), name='checkout'),
     path('update_address/<int:pk>', views.UpdateProfileFromCheckout, name='update_address'),

    path('address/', views.address, name='address'),
    path('addOrder/', views.addToOrders.as_view(), name='add_to_orders'),
    path('orders/',views.ShowOrders.as_view(),name='orders'),
    path('buy/', views.buy_now, name='buy-now'),


] 

