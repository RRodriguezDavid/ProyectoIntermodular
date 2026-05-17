"""
Vistas de gestión de pedidos: checkout e historial.
"""

from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.cart.cart import Cart
from apps.store.models import Product
from apps.printing.models import CustomSTL
from apps.users.models import UserProfile
from .models import Order, OrderItem


@login_required
def checkout(request):
    """
    Procesa la compra: crea el pedido y las líneas a partir del carrito.
    Vacía el carrito al finalizar.
    """
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('cart:detail')

    if request.method == 'POST':
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        # Crear el pedido
        order = Order.objects.create(
            user=request.user,
            total_price=cart.get_total_price(),
            status='PAID',
            direccion_envio=request.POST.get('direccion', profile.direccion),
            ciudad_envio=request.POST.get('ciudad', profile.ciudad),
            codigo_postal_envio=request.POST.get('codigo_postal', profile.codigo_postal),
            notas=request.POST.get('notas', ''),
        )

        # Crear las líneas de pedido a partir del carrito
        for item in cart:
            if item['is_custom']:
                custom = CustomSTL.objects.get(id=item['id'])
                OrderItem.objects.create(
                    order=order,
                    custom_stl=custom,
                    quantity=item['quantity'],
                    price_at_purchase=Decimal(item['price']),
                )
            else:
                product = Product.objects.get(id=item['id'])
                # Reducir stock
                product.stock -= item['quantity']
                product.save()
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price_at_purchase=Decimal(item['price']),
                )

        # Vaciar el carrito
        cart.clear()
        messages.success(request, f'¡Pedido #{order.id} realizado con éxito!')
        return redirect('orders:my_orders')

    # GET: mostrar resumen antes de confirmar
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'profile': profile,
    })


@login_required
def my_orders(request):
    """Historial de pedidos del usuario autenticado."""
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    """Detalle de un pedido concreto del usuario."""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
