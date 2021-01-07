from django.db import models
from django.contrib.auth.models import User
import string 
from django.utils.text import slugify 
import datetime


# Create your models here.

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname=models.CharField(max_length=60)
    profile_pic= models.ImageField(upload_to='admin_pics', null=True, blank=True)
    phone= models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class Patron(models.Model):
    
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    phone=models.CharField(max_length=14)
    email=models.EmailField()
    password=models.CharField(max_length=600)
    cpassword=models.CharField(max_length=600, null=True)
    address=models.CharField(max_length=100, null=True)
    last_login = models.DateTimeField('last_login', auto_now=True)
    
    def __str__(self):
        return self.firstname

    @staticmethod
    def get_user_by_phone(phone):
        try:
            return Patron.objects.get(phone=phone)
        except:
            return False

    def isExists(self):
        if Patron.objects.filter(phone=self.phone):
            return True

        else:
            return False

   
class Advertise(models.Model):
    image=models.ImageField(upload_to='pictures/%d',blank=True, null=True)
    website= models.URLField(blank=True, null=True)
    created_at = models.DateField(default=datetime.datetime.today, null=True)


    def __str__(self):
        return self.website


    @property
    def imageUrl(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
    
    class Meta:
      get_latest_by = 'created_at'
    
    



class Cat(models.Model):
    category=models.CharField(max_length=20)

    def __str__(self):
        return self.category


class SubCat(models.Model):
    sub_category=models.CharField(max_length=20)
    category=models.ForeignKey(Cat, on_delete=models.SET_NULL, blank=True, null=True)
    image=models.ImageField(upload_to='pictures/subcat',blank=True, null=True)
    image1=models.ImageField(upload_to='pictures/subcat',blank=True, null=True)
    image2=models.ImageField(upload_to='pictures/subcat',blank=True, null=True)
    slug= models.SlugField(unique=True, null=True, blank=True)


    def __str__(self):
        return self.sub_category

    @staticmethod
    def get_subcat(slug):
        return SubCat.objects.get(id=slug)

    @staticmethod
    def get_cat(slug):
        subcat=SubCat.objects.get(id=slug)
        return subcat.category
    



    @property
    def imageUrl(self):
        try:
            url=self.image.url
        except:
            url=''
        return url

    @property
    def image1Url(self):
        try:
            url=self.image1.url
        except:
            url=''
        return url

    @property
    def image2Url(self):
        try:
            url=self.image2.url
        except:
            url=''
        return url


        
class Gen(models.Model):
    gender=models.CharField(max_length=10)

    def __str__(self):
        return self.gender

class Color(models.Model):
    color=models.CharField(max_length=100)

    def __str__(self):
        return self.color

class Size(models.Model):
    size=models.CharField(max_length=40)

    def __str__(self):
        return self.size


class Product(models.Model):
    name=models.CharField(max_length=200, null=True)
    price=models.FloatField()
    category=models.ForeignKey(Cat, on_delete=models.SET_NULL, blank=True, null=True)
    slug=models.ForeignKey(SubCat, on_delete=models.SET_NULL, blank=True, null=True)
    gender=models.ForeignKey(Gen, on_delete=models.SET_NULL, blank=True, null=True)
    descrption=models.TextField(max_length=2000,blank=True, null=True)
    image=models.ImageField(upload_to='pictures',blank=True, null=True)
    image2=models.ImageField(upload_to='pictures/%d',blank=True, null=True)
    image3=models.ImageField(upload_to='pictures/%d',blank=True, null=True)
    image4=models.ImageField(upload_to='pictures/%d',blank=True, null=True)
    image5=models.ImageField(upload_to='pictures/%d',blank=True, null=True)
    pslug= models.SlugField(unique=True, null=True, blank=True)
    homefeatured= models.BooleanField(default=False,)
    on_sale= models.BooleanField(default=False)
    recent_arrival= models.BooleanField(default=False)
    offpercent=models.IntegerField(null=True)
    crossprice=models.FloatField(null=True)
    colors=models.CharField(null=True,blank=True, max_length=100)
    size=models.CharField(null=True, blank=True, max_length=30)
    viewcount=models.PositiveIntegerField(null=True, default=1)


    def __str__(self):
        return self.name


    @property
    def imageUrl(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
    
    @property
    def imageUrl2(self):
        try:
            url=self.image2.url
        except:
            url=''
        return url

    @property
    def imageUrl3(self):
        try:
            url=self.image3.url
        except:
            url=''
        return url

    @property
    def imageUrl4(self):
        try:
            url=self.image4.url
        except:
            url=''
        return url


    @property
    def imageUrl5(self):
        try:
            url=self.image5.url
        except:
            url=''
        return url


    @staticmethod
    def get_products_by_id(ids):
       return Product.objects.filter(pslug__in=ids)

    @staticmethod
    def get_product_by_id(id):
       return Product.objects.filter(pslug=id)

    @property
    def sizes_dy(self):
        if self.size == None:
            okies= 'N/A'
            return okies
        else:
            return self.size.split(',')
    
    @property
    def colors_dy(self):
        if self.colors == None:
            okies= 'N/A'
            return okies
        else:
            
            return self.colors.split(',')





class Cart(models.Model):
    customer= models.ForeignKey(Patron, on_delete=models.SET_NULL, blank=True, null=True)
    product= models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.IntegerField(default=1,null=True)
    totalprice=models.IntegerField(null=True, blank=True)
    

    def __str__(self):
        return str(self.product)

    @staticmethod
    def get_cart_by_cus(cus):
       return Cart.objects.filter(customer=cus)

    @staticmethod
    def binary_search_iterative(list, key):
        start = 0
        end = len(list) - 1
        while start <= end:
            mid = (start + end) // 2
            if list[mid] == key:

                return mid

            elif list[mid] > key:
                end = mid - 1

            else:
                start = mid + 1

        return -1

class PMethod(models.Model):
    pgateway=models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.pgateway

class OrderStatus(models.Model):
    status=models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.status



class OrderItems(models.Model):
    product= models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True, null=True)
    customer= models.ForeignKey(Patron, on_delete=models.SET_NULL, blank=True, null=True)
    # order = models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.IntegerField(default=1, null=True, blank=True)
    price=models.IntegerField(null=True)
    date = models.DateTimeField(default=datetime.datetime.now(), null=True)
    urgentstatus=models.BooleanField(default=False, null=True)
    ship=models.CharField(max_length=200, null=True)
    phone= models.CharField(max_length=20, null=True)
    orderstatus=models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, blank=True, null=True)
    pmethod=models.ForeignKey(PMethod, on_delete=models.SET_NULL, blank=True, null=True)
    payment_completed= models.BooleanField(default=False, null=True, blank=True)
    size= models.CharField(max_length=5, null=True)
    color= models.CharField(max_length=10, null=True)

    def __str__(self):
        return str(self.id)

class Comment(models.Model):
    product= models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True, null=True)
    customer= models.ForeignKey(Patron, on_delete=models.SET_NULL, blank=True, null=True)
    review= models.CharField(null=True, max_length=200)
    date = models.DateField(default=datetime.datetime.now(), null=True)


    def __str__(self):
        return str(self.product)








from.make_slug import unique_slug_generator, unique_slug_generators
from django.db.models.signals import pre_save

def pre_save_receiver(sender, instance, *args, **kwargs): 
    if not instance.pslug : 
        instance.pslug = unique_slug_generator(instance)
       
pre_save.connect(pre_save_receiver, sender = Product)



def pre_save_receivers(sender, instance, *args, **kwargs): 
    if not instance.slug :
        instance.slug = unique_slug_generators(instance)

pre_save.connect(pre_save_receivers, sender = SubCat) 


