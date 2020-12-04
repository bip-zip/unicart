from django.conf.urls import url
from . import views
from django.urls import path,include
from .views import Producty, Login, SignUp, Search, OrderList, Index
from .middleware_auth import simple_middleware




app_name='homeapp'

urlpatterns=[
    path('', Index.as_view(), name='homepage'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('cloth/', views.clothhome, name='clothhome'),
    path('electronics/', views.electrohome, name='electrohome'),
    path('search/', Search.as_view(), name='search'),
    path('search', Search.as_view(), name='search'),
    path('product/<int:slug>', Producty.as_view(), name='product'),
    path('product-detail/<str:pslug>/', views.prodetail, name='prodetail'),
    path('cart/', views.cart, name='cart'),
    path('order/<int:pslug>/', views.order, name='order'),
    path('orderlist', simple_middleware(OrderList.as_view()), name='orderlist'),

    # path('cart/', Search.as_view(), name='cart'),


    ]