from django.contrib import admin
from homeapp.models import Patron, Cat,SubCat,Gen,Product,Cart,OrderItems, Color, Size, Advertise, Admin, OrderStatus,PMethod

# admin.site.register(Patron)
# admin.site.register(Cat)
# admin.site.register(SubCat)
# admin.site.register(Gen)
# admin.site.register(Product)
# admin.site.register(Color)
# admin.site.register(Size)
# admin.site.register(Cart)
# admin.site.register(OrderItems)
# admin.site.register(Advertise)
# admin.site.register(Admin)

admin.site.register([Patron, Cat,SubCat,Gen,Product,Cart,OrderItems, Color, Size, Advertise, Admin,OrderStatus,PMethod])


