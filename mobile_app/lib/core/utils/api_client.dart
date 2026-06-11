import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:smart_interior_ai/core/constants/app_constants.dart';

class ApiClient {
  static final ApiClient _instance = ApiClient._internal();
  factory ApiClient() => _instance;

  late final Dio dio;
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  static const String _accessTokenKey = 'access_token';
  static const String _refreshTokenKey = 'refresh_token';

  ApiClient._internal() {
    dio = Dio(
      BaseOptions(
        baseUrl: AppConstants.baseUrl,
        connectTimeout: AppConstants.apiTimeout,
        receiveTimeout: AppConstants.apiTimeout,
        headers: {'Content-Type': 'application/json'},
      ),
    );

    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final token = await _storage.read(key: _accessTokenKey);
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          handler.next(options);
        },
        onError: (error, handler) async {
          final isUnauthorized = error.response?.statusCode == 401;
          final isRefreshCall =
              error.requestOptions.path.contains('/auth/refresh');

          if (isUnauthorized && !isRefreshCall) {
            final refreshed = await _refreshAccessToken();
            if (refreshed) {
              try {
                final newToken = await _storage.read(key: _accessTokenKey);
                final options = error.requestOptions;
                options.headers['Authorization'] = 'Bearer $newToken';
                final response = await dio.fetch(options);
                return handler.resolve(response);
              } catch (_) {
                // Retry failed; fall through and clear the session below.
              }
            }
            await clearTokens();
          }
          handler.next(error);
        },
      ),
    );
  }

  /// Exchanges the stored refresh token for a fresh access token.
  /// Uses a bare Dio instance so this interceptor is not invoked recursively.
  Future<bool> _refreshAccessToken() async {
    final refreshToken = await _storage.read(key: _refreshTokenKey);
    if (refreshToken == null) return false;

    try {
      final refreshDio = Dio(BaseOptions(baseUrl: AppConstants.baseUrl));
      final response = await refreshDio.post(
        '/auth/refresh',
        options: Options(headers: {'Authorization': 'Bearer $refreshToken'}),
      );

      final data = response.data as Map<String, dynamic>;
      final newAccess = data['access_token'] as String?;
      final newRefresh = data['refresh_token'] as String?;
      if (newAccess == null) return false;

      await _storage.write(key: _accessTokenKey, value: newAccess);
      if (newRefresh != null) {
        await _storage.write(key: _refreshTokenKey, value: newRefresh);
      }
      return true;
    } catch (_) {
      return false;
    }
  }

  Future<void> setToken(String token) async {
    await _storage.write(key: _accessTokenKey, value: token);
  }

  Future<void> setTokens({
    required String accessToken,
    String? refreshToken,
  }) async {
    await _storage.write(key: _accessTokenKey, value: accessToken);
    if (refreshToken != null) {
      await _storage.write(key: _refreshTokenKey, value: refreshToken);
    }
  }

  Future<void> clearToken() async {
    await _storage.delete(key: _accessTokenKey);
  }

  Future<void> clearTokens() async {
    await _storage.delete(key: _accessTokenKey);
    await _storage.delete(key: _refreshTokenKey);
  }

  Future<bool> hasToken() async {
    final token = await _storage.read(key: _accessTokenKey);
    return token != null;
  }

  /// Returns true when there is a usable session: a non-expired access token,
  /// or an expired access token that can still be refreshed via the refresh
  /// token. Clears the stored session when neither is available.
  Future<bool> hasValidSession() async {
    final accessToken = await _storage.read(key: _accessTokenKey);
    if (accessToken == null) return false;

    if (!_isJwtExpired(accessToken)) return true;

    // Access token expired - try to refresh it.
    final refreshed = await _refreshAccessToken();
    if (refreshed) return true;

    await clearTokens();
    return false;
  }

  /// Decodes a JWT and checks its `exp` claim. Returns true when the token is
  /// expired or cannot be parsed. A 30s clock-skew allowance is applied.
  bool _isJwtExpired(String token) {
    try {
      final parts = token.split('.');
      if (parts.length != 3) return true;
      final payload = utf8.decode(
        base64Url.decode(base64Url.normalize(parts[1])),
      );
      final map = jsonDecode(payload) as Map<String, dynamic>;
      final exp = map['exp'];
      if (exp is! int) return false; // No expiry claim - treat as non-expiring.
      final expiry =
          DateTime.fromMillisecondsSinceEpoch(exp * 1000, isUtc: true);
      return DateTime.now().toUtc().isAfter(
            expiry.subtract(const Duration(seconds: 30)),
          );
    } catch (_) {
      return true;
    }
  }
}
