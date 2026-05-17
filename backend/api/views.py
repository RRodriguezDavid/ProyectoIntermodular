"""
Vistas de la API REST consumida por la app Flutter.

Endpoints:
  GET  /api/v1/me/                  → datos del usuario autenticado
  GET  /api/v1/orders/              → lista de pedidos (admin: todos; cliente: los suyos)
  GET  /api/v1/orders/<id>/         → detalle de un pedido concreto
  PATCH /api/v1/orders/<id>/status/ → cambiar estado (solo admin)
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer
from apps.users.serializers import UserSerializer


# ── /api/v1/me/ ────────────────────────────────────────────────────────────────

class MeView(APIView):
    """
    Devuelve los datos del usuario autenticado.
    La app Flutter usa 'is_admin' para decidir qué controles mostrar.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ── /api/v1/orders/ ────────────────────────────────────────────────────────────

class OrderListView(APIView):
    """
    GET: devuelve la lista de pedidos.
      - Admin (is_staff=True): ve todos los pedidos de todos los usuarios.
      - Cliente (is_staff=False): ve solo sus propios pedidos.

    Los pedidos se devuelven ordenados del más reciente al más antiguo.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            queryset = Order.objects.all().prefetch_related('items__product', 'items__custom_stl')
        else:
            queryset = Order.objects.filter(user=request.user).prefetch_related('items__product', 'items__custom_stl')

        queryset = queryset.order_by('-created_at')
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)


# ── /api/v1/orders/<id>/ ───────────────────────────────────────────────────────

class OrderDetailView(APIView):
    """
    GET: devuelve el detalle completo de un pedido, incluyendo sus líneas.
      - Admin puede ver cualquier pedido.
      - Cliente solo puede ver sus propios pedidos (devuelve 404 si no es suyo).
    """
    permission_classes = [IsAuthenticated]

    def _get_order(self, pk, user):
        """Obtiene el pedido o devuelve None si no existe o no tiene permiso."""
        try:
            order = Order.objects.prefetch_related(
                'items__product', 'items__custom_stl'
            ).get(pk=pk)
        except Order.DoesNotExist:
            return None

        # Un cliente solo puede ver sus propios pedidos
        if not user.is_staff and order.user != user:
            return None

        return order

    def get(self, request, pk):
        order = self._get_order(pk, request.user)
        if order is None:
            return Response(
                {'error': 'Pedido no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderSerializer(order)
        return Response(serializer.data)


# ── /api/v1/orders/<id>/status/ ───────────────────────────────────────────────

# Estados válidos en orden de progresión
VALID_STATUSES = ['PENDING', 'PAID', 'PRINTING', 'SHIPPED', 'DELIVERED', 'CANCELLED']


class OrderStatusUpdateView(APIView):
    """
    PATCH: actualiza el campo 'status' de un pedido.
    Solo accesible por administradores (is_staff=True).

    Body JSON esperado:
        { "status": "PRINTING" }

    Respuesta: el pedido completo con el nuevo estado.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        # Solo los administradores pueden cambiar estados
        if not request.user.is_staff:
            return Response(
                {'error': 'No tienes permiso para realizar esta acción.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Validar que el pedido existe
        try:
            order = Order.objects.prefetch_related(
                'items__product', 'items__custom_stl'
            ).get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Pedido no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validar el campo status en el body
        new_status = request.data.get('status')

        if not new_status:
            return Response(
                {'error': 'El campo "status" es obligatorio.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status not in VALID_STATUSES:
            return Response(
                {
                    'error': f'Estado "{new_status}" no válido.',
                    'valid_statuses': VALID_STATUSES,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Actualizar y guardar
        order.status = new_status
        order.save(update_fields=['status', 'updated_at'])

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
