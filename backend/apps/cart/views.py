"""
Vistas del carrito de la compra.
"""

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .cart import Cart


def cart_detail(request):
    """Muestra el contenido actual del carrito con el precio total."""
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_add(request):
    """
    Añade un producto al carrito.
    Recibe item_id e is_custom por POST.
    """
    cart = Cart(request)
    item_id = int(request.POST.get('item_id'))
    quantity = int(request.POST.get('quantity', 1))
    is_custom = request.POST.get('is_custom') == 'true'

    try:
        cart.add(item_id=item_id, quantity=quantity, is_custom=is_custom)
        messages.success(request, 'Artículo añadido al carrito.')
    except Exception as e:
        messages.error(request, f'Error al añadir el artículo: {e}')

    return redirect('cart:detail')


@require_POST
def cart_remove(request):
    """Elimina un artículo del carrito."""
    cart = Cart(request)
    item_key = request.POST.get('item_key')
    cart.remove(item_key)
    messages.info(request, 'Artículo eliminado del carrito.')
    return redirect('cart:detail')


@require_POST
def cart_update(request):
    """Actualiza la cantidad de un artículo."""
    cart = Cart(request)
    item_key = request.POST.get('item_key')
    quantity = int(request.POST.get('quantity', 1))
    cart.update_quantity(item_key, quantity)
    return redirect('cart:detail')
