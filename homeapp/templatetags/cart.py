from django import template
from homeapp.models import Cart, Patron, Product
from django.shortcuts import get_object_or_404

register= template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(item, cart):
    for i in cart:
        if i == item.pslug:
            print(i)
            return True
    print('nooooooooooooooooooooooo')
    return False

    

def bubble(list):
    swap=True
    while swap:
        swap=False
        for i in range (len(list)-1):
            if list[i] > list[i+1]:
                list[i], list[i+1]= list[i+1], list[i]
                swap=True
    return (list)

   

   
    # products= cart.keys()
    # print(keys)
    # for id in keys:
    #     if id == data.pslug
    #         return True

    # return False

    # print(data)


@register.filter(name='cart_quantity')
def cart_quantity(data, cart):
    keys=cart.keys()
    for id in keys:
        if id == data.product.pslug:
            return cart.get(id)
    return 0


@register.filter(name='total_price')
def total_price(data, cart):
    return data.product.price * cart_quantity(data, cart)



@register.filter(name='all_total')
def all_total(data, cart):
    sum=0
    for i in data:
        sum = sum + total_price(i, cart)
    return sum

@register.filter(name='multiply')
def multiply(number, number1):
    return number * number1



@register.filter(name='cartnumber')
def cartnumber(customer):
    allitems=Cart.objects.filter(customer=Patron(id=customer))
    return len(allitems)

