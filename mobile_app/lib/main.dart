import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/constants/app_constants.dart';
import 'package:smart_interior_ai/presentation/screens/home_screen.dart';
import 'package:smart_interior_ai/presentation/screens/login_screen.dart';
import 'package:smart_interior_ai/presentation/screens/register_screen.dart';
import 'package:smart_interior_ai/presentation/screens/room_scan_screen.dart';
import 'package:smart_interior_ai/presentation/screens/design_result_screen.dart';
import 'package:smart_interior_ai/presentation/screens/ar_view_screen.dart';
import 'package:smart_interior_ai/presentation/screens/cost_estimation_screen.dart';
import 'package:smart_interior_ai/presentation/screens/ai_assistant_screen.dart';
import 'package:smart_interior_ai/presentation/screens/house_project_screen.dart';
import 'package:smart_interior_ai/presentation/screens/house_detail_screen.dart';
import 'package:smart_interior_ai/presentation/screens/house_cost_screen.dart';
import 'package:smart_interior_ai/presentation/screens/smart_lighting_screen.dart';
import 'package:go_router/go_router.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const ProviderScope(child: SmartInteriorApp()));
}

final _router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(path: '/', builder: (context, state) => const HomeScreen()),
    GoRoute(path: '/login', builder: (context, state) => const LoginScreen()),
    GoRoute(path: '/register', builder: (context, state) => const RegisterScreen()),
    GoRoute(path: '/scan', builder: (context, state) => const RoomScanScreen()),
    GoRoute(
      path: '/design/:roomId',
      builder: (context, state) => DesignResultScreen(
        roomId: state.pathParameters['roomId']!,
      ),
    ),
    GoRoute(
      path: '/ar/:designId',
      builder: (context, state) => ARViewScreen(
        designId: state.pathParameters['designId']!,
      ),
    ),
    GoRoute(
      path: '/cost/:designId',
      builder: (context, state) => CostEstimationScreen(
        designId: state.pathParameters['designId']!,
      ),
    ),
    GoRoute(
      path: '/assistant/:roomId',
      builder: (context, state) => AIAssistantScreen(
        roomId: state.pathParameters['roomId']!,
      ),
    ),
    GoRoute(path: '/house/new', builder: (context, state) => const HouseProjectScreen()),
    GoRoute(
      path: '/house/:projectId',
      builder: (context, state) => HouseDetailScreen(
        projectId: state.pathParameters['projectId']!,
      ),
    ),
    GoRoute(
      path: '/house/:projectId/cost',
      builder: (context, state) => HouseCostScreen(
        projectId: state.pathParameters['projectId']!,
      ),
    ),
    GoRoute(path: '/lighting', builder: (context, state) => const SmartLightingScreen()),
  ],
);

class SmartInteriorApp extends StatelessWidget {
  const SmartInteriorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: AppConstants.appName,
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: ThemeMode.system,
      routerConfig: _router,
    );
  }
}
