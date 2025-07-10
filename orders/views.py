from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from cart.models import CartItem
from .models import Order, OrderItem


@login_required
def create_order(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Il tuo carrello è vuoto")
        return redirect('cart:view_cart')

    with transaction.atomic():
        # Calcola il totale
        total = sum(
            (item.product.discounted_price if item.product.is_discounted else item.product.price) * item.quantity
            for item in cart_items
        )

        # Crea l'ordine
        order = Order.objects.create(
            user=request.user,
            total=total
        )

        # Crea gli OrderItem
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.discounted_price if cart_item.product.is_discounted else cart_item.product.price
            )

        # Svuota il carrello
        cart_items.delete()

    messages.success(request, f"Ordine #{order.id} creato con successo!")
    return redirect('orders:order_detail', order_id=order.id)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.is_cancelled:
        messages.warning(request, "Questo ordine è già stato cancellato")
        return redirect('orders:order_detail', order_id=order.id)

    with transaction.atomic():
        # Ripristina le quantità dei prodotti
        for item in order.items.all():
            item.product.quantity_available += item.quantity
            item.product.save()

        # Segna l'ordine come cancellato
        order.is_cancelled = True
        order.save()

    messages.success(request, f"Ordine #{order.id} cancellato con successo")
    return redirect('orders:order_detail', order_id=order.id)


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})