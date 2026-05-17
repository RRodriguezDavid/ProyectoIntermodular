from django.db import models
from django.contrib.auth.models import User
from apps.store.models import Product
from apps.printing.models import CustomSTL


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente de pago'),
        ('PAID', 'Pagado / En cola'),
        ('PRINTING', 'Imprimiendo'),
        ('SHIPPED', 'Enviado'),
        ('DELIVERED', 'Entregado'),
        ('CANCELLED', 'Cancelado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="Cliente")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creacion")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ultima actualizacion")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Estado")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total (euros)")

    # Datos de envio guardados en el momento de la compra
    direccion_envio = models.TextField(verbose_name="Direccion de envio")
    ciudad_envio = models.CharField(max_length=100)
    codigo_postal_envio = models.CharField(max_length=10)
    notas = models.TextField(blank=True, verbose_name="Notas del pedido")

    def __str__(self):
        return f"Pedido #{self.id} - {self.user.username} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-created_at']


class OrderItem(models.Model):
    # Guardamos el precio en el momento de la compra para que cambios futuros no afecten al historial
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    custom_stl = models.ForeignKey(CustomSTL, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Precio en el momento de compra"
    )

    def __str__(self):
        item_name = self.product.name if self.product else f"Pieza personalizada #{self.custom_stl_id}"
        return f"{item_name} x{self.quantity}"

    @property
    def subtotal(self):
        return self.price_at_purchase * self.quantity

    class Meta:
        verbose_name = "Linea de pedido"
        verbose_name_plural = "Lineas de pedido"
