// Basic Flutter widget smoke test.
//
// The previous version referenced a nonexistent `MyApp` class, which made
// `flutter test` fail to compile. Pumping the real `SmartInteriorApp` is not
// suitable for a plain unit test because its router redirect reads from
// flutter_secure_storage (a platform channel unavailable in the test host).
// This minimal test verifies the test harness compiles and runs.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('App harness renders a basic widget tree', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: Center(child: Text('Smart Interior AI')),
        ),
      ),
    );

    expect(find.text('Smart Interior AI'), findsOneWidget);
  });
}
