from django.conf.urls import url
from . import views
from django.urls import path,include
from .views import Producty, Login, SignUp, Search, OrderList, Index, KhaltiRequestView, CartManage, KhaltiVerifyView,BuyNow, AdminHome,AdminOrderView, ForgetPassword,PasswordReset, UserProfile,proDetail
from .middleware_auth import simple_middleware




app_name='homeapp'

urlpatterns=[
    path('', Index.as_view(), name='homepage'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('forget-password/', ForgetPassword.as_view(), name='forgetpassword'),
    path('password-reset/<email>/<token>/', PasswordReset.as_view(), name='passwordreset'),
    path('logout/', views.logout, name='logout'),
    path('cloth/', views.clothhome, name='clothhome'),
    path('electronics/', views.electrohome, name='electrohome'),
    path('search/', Search.as_view(), name='search'),
    path('search', Search.as_view(), name='search'),
    path('product/<int:slug>', Producty.as_view(), name='product'),
    path('product-detail/<str:pslug>/', proDetail.as_view(), name='prodetail' ),
    path('cart/', views.cart, name='cart'),
    path('manage-cart/<int:product_id>/', CartManage.as_view(), name='cartmanage'), 
    path('order/<int:pslug>/', views.order, name='order'),
    path('buynow/<int:pslug>/',BuyNow.as_view() ,name='buynow'),
    path('khalti-request/', KhaltiRequestView.as_view(), name='khaltirequest' ),
    path('khalti-verify/', KhaltiVerifyView.as_view(), name='khaltiverify' ),
    path('orderlist', OrderList.as_view(), name='orderlist'),
    path('userprofile/', UserProfile.as_view(), name='userprofile'),
    
    path('adminhome/', AdminHome.as_view(), name='adminhome' ),
    path('adminorder/<int:id>', AdminOrderView.as_view(), name='adminorder' ),
    path('changests/<int:id>/', views.changeStatus, name='changests'),
    path('cancelorder/<int:id>/', views.cancelorder, name='cancelorder'),
    

    # path('cart/', Search.as_view(), name='cart'),


    ]
