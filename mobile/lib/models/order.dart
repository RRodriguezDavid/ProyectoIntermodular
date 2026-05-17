/// Modelo de datos que mapea la respuesta JSON de la API Django
class Order {
  final int id;
  final String status;
  final String statusDisplay;
  final String createdAt;
  final String updatedAt;
  final double totalPrice;
  final List<OrderItem> items;

  const Order({
    required this.id,
    required this.status,
    required this.statusDisplay,
    required this.createdAt,
    required this.updatedAt,
    required this.totalPrice,
    required this.items,
  });

  /// Convierte el JSON de la API en un objeto Order de Dart
  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
      id: json['id'],
      status: json['status'],
      statusDisplay: json['status_display'],
      createdAt: json['created_at'],
      updatedAt: json['updated_at'],
      totalPrice: double.parse(json['total_price'].toString()),
      items: (json['items'] as List<dynamic>)
          .map((item) => OrderItem.fromJson(item))
          .toList(),
    );
  }

  /// Devuelve el color asociado al estado del pedido
  static int colorForStatus(String status) {
    switch (status) {
      case 'PENDING':
        return 0xFFF4A522; // Naranja
      case 'PAID':
        return 0xFF0066FF; // Azul
      case 'PRINTING':
        return 0xFF00C8FF; // Cian
      case 'SHIPPED':
        return 0xFF2EC27E; // Verde
      case 'DELIVERED':
        return 0xFF28A745; // Verde oscuro
      case 'CANCELLED':
        return 0xFFE63946; // Rojo
      default:
        return 0xFF6C757D; // Gris
    }
  }

  /// Lista de estados en orden para la barra de progreso
  static const List<String> progressStates = [
    'PAID',
    'PRINTING',
    'SHIPPED',
    'DELIVERED',
  ];

  /// Indice del estado actual en la barra de progreso
  int get progressIndex => progressStates.indexOf(status);
}

class OrderItem {
  final int id;
  final String productName;
  final int quantity;
  final double priceAtPurchase;

  const OrderItem({
    required this.id,
    required this.productName,
    required this.quantity,
    required this.priceAtPurchase,
  });

  factory OrderItem.fromJson(Map<String, dynamic> json) {
    return OrderItem(
      id: json['id'],
      productName: json['product_name'],
      quantity: json['quantity'],
      priceAtPurchase: double.parse(json['price_at_purchase'].toString()),
    );
  }

  double get subtotal => priceAtPurchase * quantity;
}
