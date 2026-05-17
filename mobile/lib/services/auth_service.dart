import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Servicio de autenticación JWT.
/// Guarda el token de forma segura en el dispositivo.
class AuthService {
  static const String _baseUrl =
      'http://192.168.1.37:8000/api/v1'; // localhost en emulador Android
  static const _storage = FlutterSecureStorage();
  static const _tokenKey = 'access_token';
  static const _refreshKey = 'refresh_token';
  static const _isAdminKey = 'is_admin';

  /// Hace login en la API de Django y guarda el token JWT.
  /// Devuelve true si el login fue exitoso.
  static Future<bool> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/token/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'username': username, 'password': password}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        await _storage.write(key: _tokenKey, value: data['access']);
        await _storage.write(key: _refreshKey, value: data['refresh']);

        // Obtenemos info del usuario (para saber si es admin)
        await _fetchAndStoreUserInfo(data['access']);
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  /// Obtiene el perfil del usuario y guarda si es administrador
  static Future<void> _fetchAndStoreUserInfo(String token) async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/me/'),
        headers: {'Authorization': 'Bearer $token'},
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        await _storage.write(
          key: _isAdminKey,
          value: data['is_admin'].toString(),
        );
      }
    } catch (_) {}
  }

  /// Cierra la sesión eliminando el token almacenado
  static Future<void> logout() async {
    await _storage.deleteAll();
  }

  /// Recupera el token de acceso guardado (null si no hay sesión)
  static Future<String?> getToken() async {
    return await _storage.read(key: _tokenKey);
  }

  /// Devuelve true si el usuario autenticado es administrador
  static Future<bool> isAdmin() async {
    final value = await _storage.read(key: _isAdminKey);
    return value == 'true';
  }
}
