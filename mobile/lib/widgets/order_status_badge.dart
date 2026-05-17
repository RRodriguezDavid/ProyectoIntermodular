import 'package:flutter/material.dart';
import '../models/order.dart';

/// Widget reutilizable que muestra el estado de un pedido
/// con el color e icono correspondiente.
class OrderStatusBadge extends StatelessWidget {
  final String status;
  final String statusDisplay;

  const OrderStatusBadge({
    super.key,
    required this.status,
    required this.statusDisplay,
  });

  /// Devuelve el IconData asociado al estado
  static IconData iconForStatus(String status) {
    switch (status) {
      case 'PENDING':
        return Icons.hourglass_empty;
      case 'PAID':
        return Icons.credit_card;
      case 'PRINTING':
        return Icons.print;
      case 'SHIPPED':
        return Icons.local_shipping;
      case 'DELIVERED':
        return Icons.check_circle;
      case 'CANCELLED':
        return Icons.cancel;
      default:
        return Icons.inventory_2;
    }
  }

  @override
  Widget build(BuildContext context) {
    final color = Color(Order.colorForStatus(status));

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.15),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color.withOpacity(0.4)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(iconForStatus(status), size: 14, color: color),
          const SizedBox(width: 6),
          Text(
            statusDisplay,
            style: TextStyle(
              color: color,
              fontWeight: FontWeight.bold,
              fontSize: 13,
            ),
          ),
        ],
      ),
    );
  }
}
