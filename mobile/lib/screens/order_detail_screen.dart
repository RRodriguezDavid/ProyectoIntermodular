import 'package:flutter/material.dart';
import '../models/order.dart';
import '../services/api_service.dart';
import '../widgets/order_status_badge.dart';

class OrderDetailScreen extends StatefulWidget {
  final int orderId;
  final bool isAdmin;

  const OrderDetailScreen({
    super.key,
    required this.orderId,
    required this.isAdmin,
  });

  @override
  State<OrderDetailScreen> createState() => _OrderDetailScreenState();
}

class _OrderDetailScreenState extends State<OrderDetailScreen> {
  late Future<Order> _orderFuture;

  @override
  void initState() {
    super.initState();
    _loadOrder();
  }

  void _loadOrder() {
    _orderFuture = ApiService.fetchOrderDetail(widget.orderId);
  }

  // Lista de estados que el admin puede seleccionar
  static const List<Map<String, String>> _statusOptions = [
    {'value': 'PENDING', 'label': 'Pendiente de pago'},
    {'value': 'PAID', 'label': 'Pagado / En cola'},
    {'value': 'PRINTING', 'label': 'Imprimiendo'},
    {'value': 'SHIPPED', 'label': 'Enviado'},
    {'value': 'DELIVERED', 'label': 'Entregado'},
    {'value': 'CANCELLED', 'label': 'Cancelado'},
  ];

  Future<void> _showChangeStatusDialog(Order order) async {
    String selectedStatus = order.status;

    await showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Cambiar estado del pedido'),
        content: StatefulBuilder(
          builder: (ctx, setDialogState) => Column(
            mainAxisSize: MainAxisSize.min,
            children: _statusOptions.map((opt) {
              return RadioListTile<String>(
                title: Text(opt['label']!),
                value: opt['value']!,
                groupValue: selectedStatus,
                onChanged: (val) => setDialogState(() => selectedStatus = val!),
              );
            }).toList(),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () async {
              Navigator.pop(ctx);
              await _updateStatus(selectedStatus);
            },
            child: const Text('Guardar'),
          ),
        ],
      ),
    );
  }

  Future<void> _updateStatus(String newStatus) async {
    try {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Actualizando estado...')),
      );

      await ApiService.updateOrderStatus(widget.orderId, newStatus);

      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Estado actualizado correctamente'),
          backgroundColor: Color(0xFF2EC27E),
        ),
      );

      // Refrescar el detalle
      setState(() => _loadOrder());
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Error: $e'),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: Text('Pedido #${widget.orderId}'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => setState(() => _loadOrder()),
          ),
        ],
      ),
      body: FutureBuilder<Order>(
        future: _orderFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }

          final order = snapshot.data!;

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Card de estado
                _InfoCard(
                  title: 'Estado del pedido',
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      OrderStatusBadge(
                        status: order.status,
                        statusDisplay: order.statusDisplay,
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Creado: ${_formatDate(order.createdAt)}',
                        style:
                            const TextStyle(color: Colors.grey, fontSize: 13),
                      ),
                      Text(
                        'Actualizado: ${_formatDate(order.updatedAt)}',
                        style:
                            const TextStyle(color: Colors.grey, fontSize: 13),
                      ),
                    ],
                  ),
                ),

                // Boton de admin para cambiar estado
                if (widget.isAdmin)
                  Padding(
                    padding: const EdgeInsets.only(bottom: 12),
                    child: ElevatedButton.icon(
                      icon: const Icon(Icons.edit),
                      label: const Text('Cambiar estado'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFFF4A522),
                        foregroundColor: const Color(0xFF1A1A2E),
                      ),
                      onPressed: () => _showChangeStatusDialog(order),
                    ),
                  ),

                // Articulos del pedido
                _InfoCard(
                  title: 'Articulos',
                  child: Column(
                    children: [
                      ...order.items.map((item) => Padding(
                            padding: const EdgeInsets.symmetric(vertical: 6),
                            child: Row(
                              children: [
                                Expanded(
                                  child: Text(
                                    item.productName,
                                    style: const TextStyle(fontSize: 14),
                                  ),
                                ),
                                Text(
                                  'x${item.quantity}',
                                  style: const TextStyle(
                                      color: Colors.grey, fontSize: 13),
                                ),
                                const SizedBox(width: 12),
                                Text(
                                  '${item.subtotal.toStringAsFixed(2)} EUR',
                                  style: const TextStyle(
                                      fontWeight: FontWeight.bold),
                                ),
                              ],
                            ),
                          )),
                      const Divider(),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('TOTAL',
                              style: TextStyle(fontWeight: FontWeight.bold)),
                          Text(
                            '${order.totalPrice.toStringAsFixed(2)} EUR',
                            style: const TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 18,
                              color: Color(0xFF0066FF),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  String _formatDate(String isoDate) {
    try {
      final dt = DateTime.parse(isoDate).toLocal();
      return '${dt.day.toString().padLeft(2, '0')}/${dt.month.toString().padLeft(2, '0')}/${dt.year}  ${dt.hour.toString().padLeft(2, '0')}:${dt.minute.toString().padLeft(2, '0')}';
    } catch (_) {
      return isoDate;
    }
  }
}

class _InfoCard extends StatelessWidget {
  final String title;
  final Widget child;

  const _InfoCard({required this.title, required this.child});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 1,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title.toUpperCase(),
              style: const TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.bold,
                color: Colors.grey,
                letterSpacing: 1.2,
              ),
            ),
            const SizedBox(height: 12),
            child,
          ],
        ),
      ),
    );
  }
}
