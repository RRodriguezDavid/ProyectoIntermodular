"""
URLs de la API REST (prefijo: /api/v1/).

Mapeado desde config/urls.py con:
    path('api/v1/', include('api.urls'))

Endpoints disponibles:
    POST  /api/v1/token/              → Login JWT (djangorestframework-simplejwt)
    POST  /api/v1/token/refresh/      → Renovar token JWT
    GET   /api/v1/me/                 → Datos del usuario autenticado
    GET   /api/v1/orders/             → Lista de pedidos
    GET   /api/v1/orders/<id>/        → Detalle de un pedido
    PATCH /api/v1/orders/<id>/status/ → Cambiar estado (solo admin)
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import MeView, OrderListView, OrderDetailView, OrderStatusUpdateView

urlpatterns = [
    # Autenticación JWT
    # La app Flutter hace POST aquí con {username, password}
    # y recibe {access, refresh}
    path('token/',         TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(),   name='token_refresh'),

    # Perfil del usuario autenticado
    # Flutter llama aquí justo después del login para saber si es admin
    path('me/', MeView.as_view(), name='api_me'),

    # Pedidos
    path('orders/',                OrderListView.as_view(),        name='api_orders_list'),
    path('orders/<int:pk>/',       OrderDetailView.as_view(),      name='api_order_detail'),
    path('orders/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='api_order_status'),
]
