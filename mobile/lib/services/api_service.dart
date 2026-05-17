import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/order.dart';
import 'auth_service.dart';

/// Servicio de comunicación con la API REST de Django.
/// Todos los métodos envían el token JWT en la cabecera Authorization.
class ApiService {
  static const String _baseUrl = 'http://192.168.1.37:8000/api/v1';

  /// Construye las cabeceras con el token JWT
  static Future<Map<String, String>> _headers() async {
    final token = await AuthService.getToken();
    return {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer $token',
    };
  }

  /// Obtiene la lista de pedidos del usuario autenticado.
  /// Si es admin, devuelve TODOS los pedidos.
  static Future<List<Order>> fetchOrders() async {
    final response = await http.get(
      Uri.parse('$_baseUrl/orders/'),
      headers: await _headers(),
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => Order.fromJson(json)).toList();
    } else if (response.statusCode == 401) {
      throw Exception('Sesión expirada. Vuelve a iniciar sesión.');
    } else {
      throw Exception('Error al cargar pedidos: ${response.statusCode}');
    }
  }

  /// Obtiene el detalle de un pedido concreto
  static Future<Order> fetchOrderDetail(int orderId) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/orders/$orderId/'),
      headers: await _headers(),
    );

    if (response.statusCode == 200) {
      return Order.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Pedido no encontrado.');
    }
  }

  /// [Solo Admin] Actualiza el estado de un pedido
  static Future<Order> updateOrderStatus(int orderId, String newStatus) async {
    final response = await http.patch(
      Uri.parse('$_baseUrl/orders/$orderId/status/'),
      headers: await _headers(),
      body: jsonEncode({'status': newStatus}),
    );

    if (response.statusCode == 200) {
      return Order.fromJson(jsonDecode(response.body));
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['error'] ?? 'Error al actualizar estado.');
    }
  }
}
