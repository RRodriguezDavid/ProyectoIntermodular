import 'package:flutter/material.dart';
import '../models/order.dart';
import '../services/api_service.dart';
import '../services/auth_service.dart';
import '../widgets/order_status_badge.dart';
import 'login_screen.dart';
import 'order_detail_screen.dart';

class OrdersScreen extends StatefulWidget {
  const OrdersScreen({super.key});

  @override
  State<OrdersScreen> createState() => _OrdersScreenState();
}

class _OrdersScreenState extends State<OrdersScreen> {
  late Future<List<Order>> _ordersFuture;
  bool _isAdmin = false;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  void _loadData() {
    _ordersFuture = ApiService.fetchOrders();
    AuthService.isAdmin().then((value) {
      if (mounted) setState(() => _isAdmin = value);
    });
  }

  Future<void> _logout() async {
    await AuthService.logout();
    if (!mounted) return;
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (_) => const LoginScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: Row(
          children: [
            const Icon(Icons.print, size: 20),
            const SizedBox(width: 8),
            const Text('Mis Pedidos'),
            if (_isAdmin) ...[
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  color: const Color(0xFFF4A522),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: const Text(
                  'ADMIN',
                  style: TextStyle(
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF1A1A2E),
                  ),
                ),
              ),
            ],
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => setState(() => _loadData()),
            tooltip: 'Actualizar',
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _logout,
            tooltip: 'Cerrar sesion',
          ),
        ],
      ),
      body: FutureBuilder<List<Order>>(
        future: _ordersFuture,
        builder: (context, snapshot) {
          // Cargando
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          // Error
          if (snapshot.hasError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.wifi_off, size: 64, color: Colors.grey),
                    const SizedBox(height: 16),
                    Text(
                      snapshot.error.toString(),
                      textAlign: TextAlign.center,
                      style: const TextStyle(color: Colors.grey),
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: () => setState(() => _loadData()),
                      child: const Text('Reintentar'),
                    ),
                  ],
                ),
              ),
            );
          }

          final orders = snapshot.data ?? [];

          // Sin pedidos
          if (orders.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.inbox, size: 64, color: Colors.grey),
                  SizedBox(height: 16),
                  Text('No tienes pedidos aun.',
                      style: TextStyle(color: Colors.grey, fontSize: 16)),
                ],
              ),
            );
          }

          // Lista de pedidos
          return RefreshIndicator(
            onRefresh: () async => setState(() => _loadData()),
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: orders.length,
              itemBuilder: (context, index) {
                final order = orders[index];
                return _OrderCard(
                  order: order,
                  isAdmin: _isAdmin,
                  onTap: () async {
                    await Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => OrderDetailScreen(
                          orderId: order.id,
                          isAdmin: _isAdmin,
                        ),
                      ),
                    );
                    // Refrescar al volver (por si el admin cambio el estado)
                    setState(() => _loadData());
                  },
                );
              },
            ),
          );
        },
      ),
    );
  }
}

class _OrderCard extends StatelessWidget {
  final Order order;
  final bool isAdmin;
  final VoidCallback onTap;

  const _OrderCard({
    required this.order,
    required this.isAdmin,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Cabecera
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Pedido #${order.id}',
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                    ),
                  ),
                  Text(
                    '${order.totalPrice.toStringAsFixed(2)} EUR',
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                      color: Color(0xFF0066FF),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),

              // Badge de estado
              OrderStatusBadge(
                status: order.status,
                statusDisplay: order.statusDisplay,
              ),
              const SizedBox(height: 12),

              // Barra de progreso
              if (order.status != 'CANCELLED' && order.status != 'PENDING')
                _ProgressBar(currentStatus: order.status),

              const SizedBox(height: 8),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    _formatDate(order.createdAt),
                    style: const TextStyle(color: Colors.grey, fontSize: 12),
                  ),
                  Row(
                    children: [
                      if (isAdmin)
                        const Text(
                          'Gestionar > ',
                          style: TextStyle(
                            color: Color(0xFF0066FF),
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      const Icon(Icons.chevron_right,
                          color: Colors.grey, size: 18),
                    ],
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _formatDate(String isoDate) {
    try {
      final dt = DateTime.parse(isoDate).toLocal();
      return '${dt.day.toString().padLeft(2, '0')}/${dt.month.toString().padLeft(2, '0')}/${dt.year}';
    } catch (_) {
      return isoDate;
    }
  }
}

class _ProgressBar extends StatelessWidget {
  final String currentStatus;
  static const steps = ['PAID', 'PRINTING', 'SHIPPED', 'DELIVERED'];
  static const labels = ['Pagado', 'Imprimiendo', 'Enviado', 'Entregado'];

  const _ProgressBar({required this.currentStatus});

  @override
  Widget build(BuildContext context) {
    final currentIndex = steps.indexOf(currentStatus);

    return Row(
      children: List.generate(steps.length, (i) {
        final done = i <= currentIndex;
        return Expanded(
          child: Column(
            children: [
              Container(
                height: 6,
                margin: const EdgeInsets.symmetric(horizontal: 1),
                decoration: BoxDecoration(
                  color: done ? const Color(0xFF2EC27E) : Colors.grey[300],
                  borderRadius: BorderRadius.circular(3),
                ),
              ),
              const SizedBox(height: 4),
              Text(
                labels[i],
                style: TextStyle(
                  fontSize: 9,
                  color: done ? const Color(0xFF2EC27E) : Colors.grey,
                  fontWeight: done ? FontWeight.bold : FontWeight.normal,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        );
      }),
    );
  }
}
