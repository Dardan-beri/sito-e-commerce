from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Product
from .models import CartItem
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = 0

    for item in cart_items:
        price = item.product.discounted_price if item.product.is_discounted else item.product.price
        total += price * item.quantity

    cart_count = cart_items.aggregate(total=Sum('quantity'))['total'] or 0

    return render(request, "cart/cart.html", {
        'cart_items': cart_items,
        'total': total,
        'cart_count': cart_count  # Passa il conteggio al template
    })


@csrf_exempt
@login_required
def add_to_cart(request, product_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Richiesta non valida."}, status=400)

    product = get_object_or_404(Product, id=product_id)

    if product.quantity_available <= 0:
        return JsonResponse({"success": False, "message": "Prodotto non disponibile."})

    product.quantity_available -= 1
    product.save()

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart_count = CartItem.objects.filter(user=request.user).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    return JsonResponse({
        "success": True,
        "cart_count": cart_count,
        "message": "Prodotto aggiunto al carrello"
    })


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

    cart_item.product.quantity_available += 1
    cart_item.product.save()

    cart_item.quantity -= 1

    if cart_item.quantity <= 0:
        cart_item.delete()
    else:
        cart_item.save()

    messages.success(request, "Prodotto rimosso dal carrello")
    return redirect('cart:view_cart')
