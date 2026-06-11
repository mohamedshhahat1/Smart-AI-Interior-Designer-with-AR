import 'package:flutter/foundation.dart';

class AppConstants {
  static const String appName = 'Smart Interior AI';
  static const String appVersion = '1.0.0';

  static const String _configuredBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: '',
  );

  static String get baseUrl {
    if (_configuredBaseUrl.isNotEmpty) return _configuredBaseUrl;
    if (!kIsWeb && defaultTargetPlatform == TargetPlatform.android) {
      return 'http://10.0.2.2:8000/api/v1';
    }
    return 'http://localhost:8000/api/v1';
  }

  static const int maxImageSizeMB = 20;
  static const int imageQuality = 85;
  static const double maxImageDimension = 4096;

  static const List<String> supportedStyles = [
    'Modern',
    'Scandinavian',
    'Minimalist',
    'Industrial',
    'Bohemian',
    'Mid-Century Modern',
    'Contemporary',
    'Traditional',
    'Rustic',
    'Art Deco',
    'Japanese',
    'Coastal',
    'Farmhouse',
    'Mediterranean',
  ];

  static const List<String> roomTypes = [
    'Living Room',
    'Bedroom',
    'Kitchen',
    'Bathroom',
    'Dining Room',
    'Office',
    'Studio',
  ];

  static const Duration apiTimeout = Duration(seconds: 120);
  static const Duration cacheExpiry = Duration(hours: 1);
}
