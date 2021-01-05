from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import View
from .models import Patron
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from math import ceil
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
import requests
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from homeapp.middleware_auth import simple_middleware, admin_middleware
from django.utils.decorators import method_decorator
from .utils import password_reset_token

class Index(View):
    def post(self, request):
        if request.session.get('user_id'):
            pslug = request.POST.get('data')
            return get_cart_items(request, pslug)
        else:
            return redirect('cart')

        return HttpResponseRedirect(self.request.path_info)

    def get(self, request):
        onsale = Product.objects.filter(homefeatured=True).filter(on_sale=True)
        newarrivals = Product.objects.filter(
            homefeatured=True).filter(recent_arrival=True)
        n = len(onsale)
        r = len(newarrivals)
        nSlides = n//5 + ceil((n/5)-(n//5))
        rSlides = r//5 + ceil((r/5)-(r//5))
        print('+++++++', n, nSlides)
        advertise = Advertise.objects.order_by('created_at')
        data = {'no_of_slides': nSlides, 'onsale_length': range(nSlides), 'newarrivals_length': range(
            rSlides), 'onsale': onsale, 'newarrivals': newarrivals, 'advertise': advertise}
        return render(request, 'homeapp/index.html', data)


class SignUp(View):
    def get(self, request):
        return render(request, 'homeapp/signup.html')

    def post(self, request):
        postDetail = request.POST
        firstname = postDetail.get('firstname')
        lastname = postDetail.get('lastname')
        phone = postDetail.get('phone')
        address = postDetail.get('address')
        email = postDetail.get('email')
        password = postDetail.get('password')
        cpassword = postDetail.get('cpassword')

        value = {
            'firstname': firstname,
            'lastname': lastname,
            'phone': phone,
            'email': email,
            'address': address,
            'password': password,
            'cpassword': cpassword,
        }
        customer = Patron(firstname=firstname, lastname=lastname, phone=phone,
                          address=address, email=email, password=password, cpassword=cpassword)

        error_message = self.validateUser(customer)

        if not error_message:
            customer.password = make_password(customer.password)
            customer.cpassword = make_password(customer.cpassword)
            message = ('Thank you. Mr/Mrs.'+firstname + ' ' + lastname +
                       ' for being a user of  Unicart . We will provide you quality product in cheap price.')
            send_mail('Thank you', message,
                      'herohiralaal14@gmail.com', [email])
            customer.save()
            return redirect('login')

        else:
            context = {'error': error_message, 'values': value}
            return render(request, 'homeapp/signup.html', context)

    def validateUser(self, customer):
        error_message = None
       
        if len(customer.password) < 7:
            error_message = 'Password must be of 8 letters'

        elif customer.password != customer.cpassword:
            error_message = "Password doesn't match"

        elif len(customer.phone) != 10:
            error_message = 'Phone number must be of 10 digits'

        elif customer.isExists():
            error_message = 'Phone number already taken !!'

        elif Patron.objects.filter(email=customer.email).exists():
            error_message = 'Email  already exists !!'
        return error_message


class Login(View):
    def get(self, request):
        return render(request, 'homeapp/login.html')

    def post(self, request):
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = Patron.get_user_by_phone(phone)
        error_message = None
        if user:
            result = check_password(password, user.password)
            print(result)
            if result == True:
                request.session['user_id'] = user.id
                request.session['username'] = user.firstname
                request.session['contact'] = user.phone
                request.session['address'] = user.address
                request.session['email'] = user.email
                customer = user.id
                cartitems = Cart.objects.filter(customer=Patron(id=customer))
                listi = list()
                for i in cartitems:
                    a = i.product.pslug
                    listi.append(a)

                sorted = bubble(listi)
                request.session['cart'] = sorted
                if sorted:
                    cart = sorted
                else:
                    cart = []

                request.session['cart'] = cart

                return redirect('homepage')
            else:
                error_message = 'Password incorrect !!!'
        else:
            error_message = 'No user registered to this Phone number !!'
        # print(phone,password)
        # print(user)
        return render(request, 'homeapp/login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')


class ForgetPassword(View):
    def get(self, request):
        return render(request, 'homeapp/forgetpassword.html')

    def post(self, request):
        useremail= request.POST.get('email')
        if Patron.objects.filter(email=useremail).exists():
            url = self.request.META['HTTP_HOST']
            user=Patron.objects.get(email=useremail)
            text='Click the link to reset your password. '
            html_content= url + "/password-reset/" + useremail + \
                 "/" + password_reset_token.make_token(user) + "/"
            send_mail(
                'Password Reset Link | Unicart',
                text + html_content,
                settings.EMAIL_HOST_USER,
                [useremail],
                fail_silently=False,
            )

            return render(request, 'homeapp/linksent.html')
            
        else:
            error_message = 'Email does not exists !!'
            return render(request, 'homeapp/forgetpassword.html', {'error':error_message})

    




class PasswordReset(View):
    def get(self, request,  *args, **kwargs ):
        # email=self.kwargs.get('email')
        # user= Patron.objects.get(email=email)
        # token=self.kwargs.get('token')

        return render (request, 'homeapp/passwordresetform.html')

    def post(self, request,  *args, **kwargs ):
        email=self.kwargs.get('email')
        user= Patron.objects.get(email=email)
        token=self.kwargs.get('token')
        
        if user and password_reset_token.check_token(user, token):
            password=request.POST.get('password')
            cpassword=request.POST.get('cpassword')
            message = self.formValid(password, cpassword)

            if not message:
                user.password=make_password(password)
                user.save()
                return redirect('login')
            
            else:
                return render (request, 'homeapp/passwordresetform.html', {'error':message})
        
        
        


    def formValid(self, password, cpassword):
        error_message = None
        if len(password) < 7:
            error_message = 'Password must be of 8 letters'

        elif password != cpassword:
            error_message = "Password doesn't match !"

        return error_message

        




        


def clothhome(request):
    product = SubCat.objects.filter(category=1).order_by('sub_category')
    context = {'products': product}
    return render(request, 'homeapp/clothhome.html', context)


def electrohome(request):
    product = SubCat.objects.filter(category=2).order_by('sub_category')
    context = {'products': product}
    return render(request, 'homeapp/electrohome.html', context)

class UserProfile(View):
    def get(self, request):
        userid = request.session.get('user_id')
        customer = Patron.objects.get(id=userid)
        orders = OrderItems.objects.filter(customer=userid).order_by('-id')
        context={'user':customer, 'orders':orders}
        return render(request, 'homeapp/userprofile.html', context)


class Producty(View):
    def post(self, request, slug):
        if request.session.get('user_id'):
            pslug = request.POST.get('data')
            return get_cart_items(request, pslug)

        else:
            return redirect('cart')

    def get(self, request, slug):
        dhakal = None
        genders = Gen.objects.all()
        gender_id = request.GET.get('cate')
        cat= SubCat.get_cat(slug)
        print('-----------------------',cat)
        if gender_id:
            products = Product.objects.filter(slug_id=slug, gender=gender_id)
            subcat = SubCat.get_subcat(slug)
            paginator= Paginator(products, 10)
            page_number = request.GET.get('page')
            dhakal= paginator.get_page(page_number)
            
        else:
            products = Product.objects.filter(slug_id=slug)
            subcat = SubCat.get_subcat(slug)
            paginator= Paginator(products, 10)
            page_number = request.GET.get('page')
            dhakal= paginator.get_page(page_number)

        return render(request, 'homeapp/product.html', {'products': dhakal, 'genders': genders, 'subcat': subcat, 'cat': cat})


def prodetail(request, pslug):
    if request.method == 'GET':
        data = Product.objects.filter(pslug=pslug)
        pro=Product.objects.get(pslug=pslug)
        pro.viewcount += 1
        pro.save()
        cat= SubCat.get_cat(pro.slug.id)
        return render(request, 'homeapp/pdetail.html', {'details': data, 'cat': cat})
    else:
        if request.session.get('user_id'):
            pslug = request.POST.get('data')
            return get_cart_items(request, pslug)
        else:
            return redirect('cart')

        return HttpResponseRedirect(self.request.path_info)


def cart(request):
    if request.method == "GET":

        if request.session.get('user_id'):
            customer = request.session.get('user_id')
            cart2 = request.session.get('cart')
            customer = Patron(id=customer)
            product = Cart.objects.filter(customer=customer).order_by('-id')

            paginator= Paginator(product, 15)
            page_number = request.GET.get('page')
            products= paginator.get_page(page_number)
            return render(request, 'homeapp/cart.html', {'products': products})

        else:
            msg1 = 'You have not logged in yet! '
            return render(request, 'homeapp/cart.html', {'msg1': msg1})

    else:
        return render(request, 'homeapp/index.html')


class CartManage(View):
    def get(self, request, *args, **kwargs):
        customer = request.session.get('user_id')
        cart2 = request.session.get('cart')
        cart_id=self.kwargs['product_id']
        cart = Cart.objects.get(
                    id=cart_id)
        product=cart.product
        action=request.GET.get('action')
        cart.totalprice = product.price

        if action == 'plus':
            cart.quantity += 1
            cart.totalprice = product.price
            cart.totalprice = product.price * cart.quantity
            cart.save()
            
        elif action == 'minus':
            if cart.quantity == 1:
                cart.quantity = 1
                cart.totalprice = product.price * cart.quantity
                cart.save()
            else:
                cart.quantity -= 1
                cart.totalprice = product.price * cart.quantity
                cart.save()

        elif action == 'rem':
            cart.delete()
            cart2.remove(product.pslug)
            request.session['cart'] = cart2

        print('we all are done. ', cart_id, action)
        return redirect('homeapp:cart')

class Search(View):

    def post(self, request):
        if request.session.get('user_id'):
            pslug = request.POST.get('data')
            return get_cart_items(request, pslug)
        else:
            return redirect('cart')

        return HttpResponseRedirect(self.request.path_info)

    def get(self, request):
        query = request.GET['query']

        if len(query) > 20:
            messages.warning(
                request, 'Query is too long to read, you know I am lazy.🥱')
            search_products = Product.objects.none()

        elif len(query) == 0 or len(query) < 2:
            search_products = Product.objects.none()
            messages.error(
                request, 'Give a well keyword so that i can fetch matching data..')

        else:
            # searchbyName = Product.objects.filter(name__icontains=query)
            # searchbyDesc = Product.objects.filter(descrption__icontains=query)
            # searchbyPrice = Product.objects.filter(price__icontains=query)
            # search_products = searchbyName.union(searchbyDesc, searchbyPrice)
            products=Product.objects.filter(Q(name__icontains=query) | Q(descrption__icontains=query) | Q(price__icontains=query) )
        paginator= Paginator(products, 10)
        page_number = request.GET.get('page')
        search_products= paginator.get_page(page_number)
        sproducts = {'sproduct': search_products, 'query': query}
        return render(request, 'homeapp/search.html', sproducts)


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

def order(request, pslug):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        urgent = request.POST.get('urgent')
        paymentid = request.POST.get('payment')
        payment = PMethod.objects.get(id=paymentid)
        color = request.POST.get('color')
        size = request.POST.get('size')
        customer = request.session.get('user_id')
        email = request.session.get('email')
        
        cart_product = Cart.objects.get(id=pslug)
        product=cart_product.product
        orderitem=product.name
        ostatus= OrderStatus.objects.get(id=1)
        # product= Product.get_product_by_id(pslug=pslug)
        # products=Product.get_products_by_id(list(cart.keys()))

        # for product in products:
        #     order= OrderItems(customer=Patron(id= customer),
        #                      product=product, price=product.price,urgent=urgent,
        #                      ship=address, phone=phone)
        #     order.save()
        
        if urgent:
            final_price = cart_product.totalprice + 200
            order = OrderItems(customer=Patron(id=customer),
                           product=product, price=final_price, urgentstatus=urgent,quantity=cart_product.quantity,
                           pmethod=payment, color=color, size=size ,ship=address, phone=phone, payment_completed=False, orderstatus=ostatus)
            order.save()
        else:
            final_price = cart_product.totalprice + 50
            order = OrderItems(customer=Patron(id=customer),
                           product=product, price=final_price, urgentstatus=urgent,quantity=cart_product.quantity,
                           pmethod=payment, color=color, size=size ,ship=address, phone=phone, payment_completed=False, orderstatus=ostatus)
            order.save()
        
        pm = request.POST.get('payment')

        
        if urgent:
            if pm == '2':
                return redirect(reverse('homeapp:khaltirequest') + '?o_id=' + str(order.id))
            message = ('Thank you for ordering ' + orderitem +
                       ' from Unicart. Your product will be shipped within 2-3 hours.')
            send_mail('Thank you', message,
                      'herohiralaal14@gmail.com', [email])
           
                      
        else:
            if pm == '2':
                return redirect(reverse('homeapp:khaltirequest') + '?o_id=' + str(order.id))
            message = ('Thank you for ordering ' + orderitem +
                       ' from Unicart. Your product will be shipped within 2-3 days.')
            send_mail('Thank you', message,
                      'herohiralaal14@gmail.com', [email])

            
        return redirect('orderlist')

    else:
        customer = request.session.get('user_id')
        product = Cart.objects.get(id=pslug)
        cat= SubCat.get_cat(product.product.slug.id)
        # product = get_object_or_404(cart, product=pslug)

        # product=Cart.objects.filter()
        return render(request, 'homeapp/order.html', {'product': product, 'cat':cat})
class BuyNow(View):
    def get(self, request, *args, **kwargs):
        pslug= self.kwargs['pslug']
        product= Product.objects.get(id=pslug)
        cat= SubCat.get_cat(product.slug.id)
        return render(request, 'homeapp/buynow.html', {'product': product,'cat':cat})

    
    def post(self, request, *args, **kwargs):
        pslug= self.kwargs['pslug']
        product= Product.objects.get(id=pslug)
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        urgent = request.POST.get('urgent')
        paymentid = request.POST.get('payment')
        payment = PMethod.objects.get(id=paymentid)
        ostatus= OrderStatus.objects.get(id=1)
        color = request.POST.get('color')
        size = request.POST.get('size')
        customer = request.session.get('user_id')
        email = request.session.get('email')
        orderitem=product.name
        # product= Product.get_product_by_id(pslug=pslug)
        # products=Product.get_products_by_id(list(cart.keys()))

        # for product in products:
        #     order= OrderItems(customer=Patron(id= customer),
        #                      product=product, price=product.price,urgent=urgent,
        #                      ship=address, phone=phone)
        #     order.save()

        if urgent:
            final_price = product.price + 200
            order = OrderItems(customer=Patron(id=customer),
                           product=product, price=final_price, urgentstatus=urgent,quantity=1,
                           pmethod=payment, color=color, size=size ,ship=address, phone=phone, payment_completed=False, orderstatus=ostatus)
            order.save()
        else:
            final_price = product.price + 50
            order = OrderItems(customer=Patron(id=customer),
                           product=product, price=final_price, urgentstatus=urgent,quantity=1,
                           pmethod=payment, color=color, size=size ,ship=address, phone=phone, payment_completed=False, orderstatus=ostatus)
            order.save()
        
        pm = request.POST.get('payment')

        
        if urgent:
            if pm == '2':
                return redirect(reverse('homeapp:khaltirequest') + '?o_id=' + str(order.id))
            message = ('Thank you for ordering ' + orderitem +
                       ' from Unicart. Your product will be shipped within 2-3 hours.')
            send_mail('Thank you', message,
                      'herohiralaal14@gmail.com', [email])
           
                      
        else:
            if pm == '2':
                return redirect(reverse('homeapp:khaltirequest') + '?o_id=' + str(order.id))
            message = ('Thank you for ordering ' + orderitem +
                       ' from Unicart. Your product will be shipped within 2-3 days.')
            send_mail('Thank you', message,
                      'herohiralaal14@gmail.com', [email])
                      
        return redirect('orderlist')

class KhaltiRequestView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        order = OrderItems.objects.get(id=o_id)
        data = {
            "order": order
        }
        return render(request, 'homeapp/khaltirequest.html', data)


class KhaltiVerifyView(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        amount = request.GET.get('amount')
        order = request.GET.get('order')
        print(token, amount, order)
        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
        }
        headers = {
            "Authorization": "Key test_secret_key_e870cfff05194c559c7e89cab66ab904"
        }

        order_obj= OrderItems.objects.get(id=order)
        response = requests.post(url, payload, headers=headers)
        res_dict= response.json()
        print(res_dict)
        if res_dict.get('idx'):
            success=True
            order_obj.payment_completed = True
            oi= order_obj.product
            orderitem= oi.name
            customer= order_obj.customer
            email=customer.email
            if order_obj.urgentstatus:
                message = ('Thank you for ordering ' + orderitem +
                        ' from Unicart. Your payment has been recieved via Khalti. Your product will be shipped within 2-3 hours.')
                send_mail('Thank you', message,
                        'herohiralaal14@gmail.com', [email])
            else:
                message = ('Thank you for ordering ' + orderitem +
                        ' from Unicart. Your payment has been recieved via Khalti. Your product will be shipped within 2-3 days.')
                send_mail('Thank you', message,
                        'herohiralaal14@gmail.com', [email])

            order_obj.save()
        else:
            success=False
        
        data = {
            'success': success
        }
        return JsonResponse(data)


class OrderList(View):
    @method_decorator(simple_middleware)
    def get(self, request):
        customer = request.session.get('user_id')
        orders = OrderItems.objects.filter(customer=customer).order_by('-id')
        return render(request, 'homeapp/orderlist.html', {'orders': orders})




class AdminLogin(View):
    # template_name= 'homeapp/admin/adminlogin.html'
    # success_url = reverse_lazy('homeapp:adminhome')
    def get(self, request):
        return render (request, 'homeapp/admin/adminlogin.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        usr=authenticate(username=username, password=password)
        error_message = None
        if usr is not None:
            request.session['admin_id'] =usr.id
            return redirect('homeapp:adminhome')
        
        else:
            error_message = 'Invalid Crediantials'
            
        return render (request, 'homeapp/admin/adminlogin.html',{'error': error_message})




class AdminHome(View):
    @method_decorator(admin_middleware)
    def get(self, request):
        orders= OrderItems.objects.filter(urgentstatus=None).order_by('-id')
        urgents= OrderItems.objects.filter(urgentstatus=True).order_by('-id')
        data={'orders':orders,'urgents':urgents}
        return render (request, 'homeapp/admin/adminhome.html', data)


class AdminOrderView(View):
    
    def get(self, request, *args, **kwargs):
        okay=self.kwargs['id']
        order= OrderItems.objects.get(id=okay)
        data={'order':order}
        return render (request, 'homeapp/admin/orderview.html', data)

def changeStatus(request, id):
    if request.method == 'GET':
        order= OrderItems.objects.get(id=id)
        action= request.GET.get('action')
        if action == "1":
            oid= 2
            orderid=OrderStatus.objects.get(id=oid)
            order.orderstatus = orderid
            order.save()

        elif action == "2":
            oid= 3
            orderid=OrderStatus.objects.get(id=oid)
            order.orderstatus = orderid
            order.save()

        elif action == "3":
            oid= 4
            orderid=OrderStatus.objects.get(id=oid)
            order.orderstatus = orderid
            order.save()

        elif action == "4":
            oid= 5
            orderid=OrderStatus.objects.get(id=oid)
            order.orderstatus = orderid
            order.save()
        
        elif action == "5":
            oid= 1
            orderid=OrderStatus.objects.get(id=oid)
            order.orderstatus = orderid
            order.save()

            
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))










def cancelorder(request, id):
    if request.method == 'GET':
        order= OrderItems.objects.get(id=id)
        action= request.GET.get('action')
        if action == "1":
            oid= 5
            orderid=OrderStatus.objects.get(id=oid)
            order.orderstatus = orderid
            order.save()

        elif action == "2":
            oid= 5
            orderid=OrderStatus.objects.get(id=oid)
            order.orderstatus = orderid
            order.save()

        elif action == "3":
            oid= 5
            orderid=OrderStatus.objects.get(id=oid)
            order.orderstatus = orderid
            order.save()

        elif action == "4":
            oid= 5
            orderid=OrderStatus.objects.get(id=oid)
            order.orderstatus = orderid
            order.save()
        
        elif action == "5":
            oid= 5
            orderid=OrderStatus.objects.get(id=oid)
            order.orderstatus = orderid
            order.save()

            
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def bubble(list):
    swap = True
    while swap:
        swap = False
        for i in range(len(list)-1):
            if list[i] > list[i+1]:
                list[i], list[i+1] = list[i+1], list[i]
                swap = True
    return (list)


def get_cart_items(request, pslug):
    customer = request.session.get('user_id')
    cart1 = request.session.get('cart')
    
    product = get_object_or_404(Product, pslug=pslug)
    pslugo = product.pslug
    print('--------------------------------->', product)
    allitems = Cart.objects.filter(customer=Patron(id=customer))
    listi = list()
    for i in allitems:
        a = i.product.pslug
        listi.append(a)

    sorted = bubble(listi)
    search = Cart.binary_search_iterative(sorted, pslugo)
    print('==================>', search)
    if search == -1:
        cart = Cart(customer=Patron(id=customer), product=product, totalprice=product.price)
        cart.save()
        cart1.append(product.pslug)
        request.session['cart'] = cart1
        print(cart1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
