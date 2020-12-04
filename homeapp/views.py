from django.shortcuts import render,get_object_or_404, redirect,HttpResponseRedirect, HttpResponse
from .models import *
from django.contrib import messages
from django.views import View
from .models import Patron
from django.contrib.auth.hashers import make_password, check_password

class Index(View):
    def post(self,request):
        data=request.POST.get('data')
        cart=request.session.get('cart')
        remove= request.POST.get('remove')
        request.session['cart']=cart
        return HttpResponseRedirect(self.request.path_info)


    def get(self, request):
        cart= request.session.get('cart')
        if not cart:
            request.session.cart={}

        dhakal= Product.objects.filter(homefeatured=True)
        return render(request,'homeapp/index.html',{'products':dhakal})



class SignUp(View):
    def get(self, request):
        return render(request, 'homeapp/signup.html')

    def post(self, request):
        postDetail=request.POST
        firstname=postDetail.get('firstname')
        lastname=postDetail.get('lastname')
        phone=postDetail.get('phone')
        email=postDetail.get('email')
        password=postDetail.get('password')
        cpassword=postDetail.get('cpassword')

        value={
            'firstname':firstname,
            'lastname':lastname,
            'phone':phone,
            'email':email,
            'password':password,
            'cpassword':cpassword
        }
        customer=Patron(firstname=firstname, lastname=lastname, phone=phone, email=email, password=password, cpassword=cpassword)

        error_message=self.validateUser(customer)

        if not error_message:
            customer.password= make_password(customer.password)
            customer.cpassword= make_password(customer.cpassword)
            customer.save()
            return redirect('login')

        else:
            context={'error':error_message, 'values':value}
            return render(request, 'homeapp/signup.html',context)


    def validateUser(self, customer):
        error_message=None
        if len(customer.password) < 7:
            error_message='Password must be of 8 letters'
                
        elif customer.password != customer.cpassword:
            error_message="Password doesn't match"

        elif len(customer.phone) != 10:
            error_message='Phone number must be of 10 digits'
            
        elif customer.isExists():
            error_message='Phone number already taken !!'
        return error_message
            

class Login(View):
    def get(self, request):
        return render(request,'homeapp/login.html')

    def post(self, request):
        phone= request.POST.get('phone')
        password = request.POST.get('password')
        user=Patron.get_user_by_phone(phone)
        error_message=None
        if user:
            result = check_password(password, user.cpassword)
            print(result)
            if result == True:
                request.session['user_id']= user.id
                request.session['username']=user.firstname
                request.session['contact']= user.phone

                return redirect('homepage')
            else:
                error_message='Password incorrect !!!'
        else:
            error_message='No user registered to this Phone number !!'
        # print(phone,password)
        # print(user)
        return render(request, 'homeapp/login.html', {'error':error_message})


def logout(request):
    request.session.clear()
    return redirect('login')
    


def clothhome(request):
    product= SubCat.objects.filter(category=1).order_by('sub_category')
    context={'products':product}
    return render (request,'homeapp/clothhome.html',context)


def electrohome(request):
    product= SubCat.objects.filter(category=2).order_by('sub_category')
    context={'products':product}
    return render (request,'homeapp/electrohome.html',context)

class Producty(View):
    def post(self,request, slug):
        return HttpResponseRedirect(self.request.path_info)


    def get(self, request, slug):
        dhakal= Product.objects.filter(slug_id=slug)
        return render(request,'homeapp/product.html',{'products':dhakal})


def prodetail(request, pslug):
    data=Product.objects.filter(pslug=pslug)
    return render(request,'homeapp/pdetail.html',{'details':data})


def cart(request):
    if request.method == "GET": 

        if request.session.get('user_id'):
            customer = request.session.get('user_id')
            customer=Patron(id=customer)
            products= Cart.objects.filter(customer=customer)
            return render(request, 'homeapp/cart.html',{'products':products})

        else:
            msg1='You have not logged in yet! '
            return render(request, 'homeapp/cart.html', {'msg1':msg1})

    else:
        return render(request, 'homeapp/index.html')


class Search(View):

    def post(self,request):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    def get(self, request):
        query=request.GET['query']
        
        if len(query)>20:
            messages.warning(request,'Query is too long to read, you know I am lazy.🥱')
            search_products=Product.objects.none()
        
        elif len(query)==0 or len(query)<2:
            search_products=Product.objects.none()
            messages.error(request,'Give a well keyword so that i can fetch matching data..')

        else:
            searchbyName=Product.objects.filter(name__icontains=query)
            searchbyDesc=Product.objects.filter(descrption__icontains=query)
            searchbyPrice=Product.objects.filter(price__icontains=query)
            search_products=searchbyName.union(searchbyDesc,searchbyPrice)

        sproducts={'sproduct': search_products, 'query':query}
        return render (request,'homeapp/search.html', sproducts)


# class CheckOut(View):
#     def post(self, request, pslug):
#         address=request.POST.get('address')
#         phone= request.POST.get('phone')
#         urgent= request.POST.get('urgent')
#         customer=request.session.get('user_id')
#         cart= request.session.get('cart')
#         # product= get_object_or_404(Product, pslug=pslug)
#         product= Product.get_product_by_id(cart.key(pslug))
#         # products=Product.get_products_by_id(list(cart.keys()))
#         print(cart, products)

#         # for product in products:
#         #     order= OrderItems(customer=Patron(id= customer), 
#         #                      product=product, price=product.price,urgent=urgent, 
#         #                      ship=address, phone=phone)
#         #     order.save()
        
#         order= OrderItems(customer=Patron(id= customer), 
#                               product=product.name, price=product.price,urgent=urgent, 
#                              ship=address, phone=phone)
#         order.save()
#         return redirect('cart')

def order(request,pslug):
    if request.method == 'POST':
        address=request.POST.get('address')
        phone= request.POST.get('phone')
        urgent= request.POST.get('urgent')
        customer=request.session.get('user_id')
        product= get_object_or_404(Product, id=pslug)
        # product= Product.get_product_by_id(pslug=pslug)
        # products=Product.get_products_by_id(list(cart.keys()))

        # for product in products:
        #     order= OrderItems(customer=Patron(id= customer), 
        #                      product=product, price=product.price,urgent=urgent, 
        #                      ship=address, phone=phone)
        #     order.save()
        
        order= OrderItems(customer=Patron(id= customer), 
                              product=product, price=product.price,urgentstatus=urgent, 
                             ship=address, phone=phone)
        order.save()
        return redirect('orderlist')

    else:
        customer=request.session.get('user_id')
        cart=Cart.objects.filter(customer=customer)
        product=get_object_or_404(cart,product=pslug)
        # product=Cart.objects.filter()
        return render(request, 'homeapp/order.html',{'product':product})


class OrderList(View):
    def get(self,request):
        customer = request.session.get('user_id')
        orders= OrderItems.objects.filter(customer=customer)
        return render(request, 'homeapp/orderlist.html',{'orders':orders})