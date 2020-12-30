"""unicart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from homeapp import views
from homeapp.views import Producty, SignUp, Login, OrderList, Index, KhaltiRequestView, KhaltiVerifyView, CartManage, BuyNow, AdminLogin, AdminHome, AdminOrderView

from django.conf.urls.static import static
from django.conf import settings
from homeapp.middleware_auth import simple_middleware


urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', include('homeapp.urls')),
    path ('', Index.as_view(), name='homepage'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path ('logout/', include('homeapp.urls')),
    path('cloth/', views.clothhome, name='clothhome'),
    path('cart/', views.cart, name='cart'),
    path('manage-cart/<int:product_id>/', CartManage.as_view(), name='cartmanage'), 
    path ('search/', include('homeapp.urls')),
    path ('search/', include('homeapp.urls')),
    path ('search/search', include('homeapp.urls')),
    path ('electronics/', include('homeapp.urls')),
    path('product/',Producty.as_view() ,name='product'),
    path ('product-detail/', include('homeapp.urls')),
    path ('order/', include('homeapp.urls')),
    path('buynow/<int:pslug>/',BuyNow.as_view() ,name='buynow'),

    path('khalti-request/', KhaltiRequestView.as_view(), name='khaltirequest' ),
    path('khalti-verify/', KhaltiVerifyView.as_view(), name='khaltiverify' ),

    path('orderlist/', simple_middleware(OrderList.as_view()), name='orderlist'),
    path('adminlogin/', AdminLogin.as_view(), name='adminlogin' ),
    path('adminhome/', AdminHome.as_view(), name='adminhome' ),
    path('adminorder/<int:id>/', AdminOrderView.as_view(), name='adminorder' ),
    path('changests/<int:id>/', views.changeStatus, name='changests'),



    
]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)