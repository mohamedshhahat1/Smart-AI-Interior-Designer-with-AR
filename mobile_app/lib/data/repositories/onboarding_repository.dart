import 'package:shared_preferences/shared_preferences.dart';

class OnboardingRepository {
  static const _completedKey = 'onboarding_completed';

  Future<bool> isCompleted() async {
    final preferences = await SharedPreferences.getInstance();
    return preferences.getBool(_completedKey) ?? false;
  }

  Future<void> complete() async {
    final preferences = await SharedPreferences.getInstance();
    await preferences.setBool(_completedKey, true);
  }
}
