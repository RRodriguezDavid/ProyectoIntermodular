from decimal import Decimal
from apps.store.models import Product
from apps.printing.models import CustomSTL


class Cart:
    """
    Gestiona el carrito de compra usando la sesion de Django.
    Soporta productos de tienda y piezas personalizadas (STL subidos por el usuario).
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, item_id, quantity=1, is_custom=False):
        # Usamos claves distintas para diferenciar productos de tienda y STLs personalizados
        item_key = f"custom_{item_id}" if is_custom else f"prod_{item_id}"

        if item_key not in self.cart:
            if is_custom:
                obj = CustomSTL.objects.get(id=item_id)
                price = str(obj.calculated_price)
                name = f"Impresion personalizada #{item_id}"
            else:
                obj = Product.objects.get(id=item_id)
                price = str(obj.base_price)
                name = obj.name

            self.cart[item_key] = {
                'id': item_id,
                'name': name,
                'quantity': 0,
                'price': price,
                'is_custom': is_custom,
            }

        self.cart[item_key]['quantity'] += quantity
        self.save()

    def remove(self, item_key):
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def update_quantity(self, item_key, quantity):
        if item_key in self.cart:
            if quantity <= 0:
                self.remove(item_key)
            else:
                self.cart[item_key]['quantity'] = quantity
                self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        if 'cart' in self.session:
            del self.session['cart']
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        for key, item in self.cart.items():
            item['key'] = key
            item['subtotal'] = Decimal(item['price']) * item['quantity']
            yield item
