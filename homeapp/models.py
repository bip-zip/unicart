from django.db import models
from django.contrib.auth.models import User
import string 
from django.utils.text import slugify 
import datetime

# Create your models here.

class Patron(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    phone=models.CharField(max_length=14)
    email=models.EmailField()
    password=models.CharField(max_length=600)
    cpassword=models.CharField(max_length=600, null=True)

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
    homefeatured= models.BooleanField(default=False)
    offpercent=models.IntegerField(null=True)
    crossprice=models.FloatField(null=True)
    colors=models.ManyToManyField('Color', null=True)
    size=models.ManyToManyField('Size', null=True)


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

class Color(models.Model):
    color=models.CharField(max_length=10)

    def __str__(self):
        return self.color

class Size(models.Model):
    size=models.CharField(max_length=10)

    def __str__(self):
        return self.size



class Cart(models.Model):
    customer= models.ForeignKey(Patron, on_delete=models.SET_NULL, blank=True, null=True)
    product= models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.IntegerField(default=1,null=True)
    

    def __str__(self):
        return str(self.product)

    @staticmethod
    def get_cart_by_cus(cus):
       return Cart.objects.filter(customer=cus)

class OrderItems(models.Model):
    product= models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True, null=True)
    customer= models.ForeignKey(Patron, on_delete=models.SET_NULL, blank=True, null=True)
    # order = models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.IntegerField(default=1, null=True, blank=True)
    price=models.IntegerField(null=True)
    date = models.DateField(default=datetime.datetime.today, null=True)
    urgentstatus=models.BooleanField(default=False, null=True)
    ship=models.CharField(max_length=200, null=True)
    phone= models.CharField(max_length=20, null=True)
    status=models.BooleanField(default=False)






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


