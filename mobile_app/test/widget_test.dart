// Basic Flutter widget smoke test.
//
// The previous version referenced a nonexistent `MyApp` class, which made
// `flutter test` fail to compile. Pumping the real `SmartInteriorApp` is not
// suitable for a plain unit test because its router redirect reads from
// flutter_secure_storage (a platform channel unavailable in the test host).
// This minimal test verifies the test harness compiles and runs.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:smart_interior_ai/data/models/furniture_model.dart';
import 'package:smart_interior_ai/presentation/widgets/furniture_card.dart';

void main() {
  testWidgets('App harness renders a basic widget tree', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(body: Center(child: Text('Smart Interior AI'))),
      ),
    );

    expect(find.text('Smart Interior AI'), findsOneWidget);
  });

  testWidgets('Furniture card renders recommendation details', (
    WidgetTester tester,
  ) async {
    final furniture = FurnitureModel(
      id: 'chair-1',
      name: 'Oak Lounge Chair',
      category: 'chair',
      style: 'modern',
      price: 249,
      rating: 4.7,
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 300,
            child: FurnitureCard(furniture: furniture),
          ),
        ),
      ),
    );

    expect(find.text('Oak Lounge Chair'), findsOneWidget);
    expect(find.text('chair'), findsOneWidget);
    expect(find.text(r'$249'), findsOneWidget);
    expect(find.text('4.7'), findsOneWidget);
  });
}
