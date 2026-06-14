import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:smart_interior_ai/data/repositories/onboarding_repository.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('onboarding completion persists', () async {
    SharedPreferences.setMockInitialValues({});
    final repository = OnboardingRepository();

    expect(await repository.isCompleted(), isFalse);

    await repository.complete();

    expect(await repository.isCompleted(), isTrue);
  });
}
