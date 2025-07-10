from django.shortcuts import render
from .models import Product
from django.db.models import Sum
from cart.models import CartItem

def home_view(request):
    products = Product.objects.all()
    cart_count = 0

    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).aggregate(
            total=Sum('quantity')
        )['total'] or 0

    return render(request, 'home.html', {
        'products': products,
        'cart_count': cart_count
    })