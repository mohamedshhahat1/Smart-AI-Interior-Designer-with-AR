import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:smart_interior_ai/presentation/screens/onboarding_screen.dart';

void main() {
  testWidgets('onboarding moves through all four pages and finishes', (
    tester,
  ) async {
    var finished = false;

    await tester.pumpWidget(
      MaterialApp(
        home: OnboardingScreen(
          onFinished: () async => finished = true,
        ),
      ),
    );
    await tester.pump(const Duration(milliseconds: 100));

    expect(find.text('Design Your Dream Space with AI'), findsOneWidget);

    await tester.tap(find.byKey(const Key('onboarding_next')));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 700));
    expect(find.text('AI Understands Your Space'), findsOneWidget);

    await tester.tap(find.byKey(const Key('onboarding_next')));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 700));
    expect(find.text('See Designs in Augmented Reality'), findsOneWidget);

    await tester.tap(find.byKey(const Key('onboarding_next')));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 700));
    expect(
        find.text('Your Personal Interior Design Assistant'), findsOneWidget);

    await tester.tap(find.byKey(const Key('onboarding_get_started')));
    await tester.pump();
    expect(finished, isTrue);
  });

  testWidgets('skip finishes onboarding immediately', (tester) async {
    var finished = false;

    await tester.pumpWidget(
      MaterialApp(
        home: OnboardingScreen(
          onFinished: () async => finished = true,
        ),
      ),
    );
    await tester.pump(const Duration(milliseconds: 100));

    await tester.tap(find.byKey(const Key('onboarding_skip')));
    await tester.pump();

    expect(finished, isTrue);
  });

  testWidgets('onboarding fits a narrow phone in dark mode', (tester) async {
    tester.view.physicalSize = const Size(390, 844);
    tester.view.devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(
      MaterialApp(
        theme: ThemeData(useMaterial3: true, brightness: Brightness.light),
        darkTheme: ThemeData(useMaterial3: true, brightness: Brightness.dark),
        themeMode: ThemeMode.dark,
        home: OnboardingScreen(onFinished: () async {}),
      ),
    );
    await tester.pump(const Duration(milliseconds: 100));

    expect(find.text('Design Your Dream Space with AI'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
