import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:smart_interior_ai/core/theme/app_theme.dart';
import 'package:smart_interior_ai/core/constants/app_constants.dart';
import 'package:smart_interior_ai/core/utils/api_client.dart';
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
import 'package:smart_interior_ai/presentation/screens/feng_shui_screen.dart';
import 'package:smart_interior_ai/presentation/screens/furniture_recommendation_screen.dart';
import 'package:smart_interior_ai/presentation/screens/seasonal_theme_screen.dart';
import 'package:smart_interior_ai/presentation/screens/pet_friendly_screen.dart';
import 'package:smart_interior_ai/presentation/screens/walkthrough_3d_screen.dart';
import 'package:smart_interior_ai/presentation/screens/profile_screen.dart';
import 'package:go_router/go_router.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const ProviderScope(child: SmartInteriorApp()));
}

const _publicRoutes = ['/login', '/register'];

final _router = GoRouter(
  initialLocation: '/',
  redirect: (context, state) async {
    final isLoggedIn = await ApiClient().hasValidSession();
    final isPublicRoute = _publicRoutes.contains(state.matchedLocation);

    if (!isLoggedIn && !isPublicRoute) return '/login';
    if (isLoggedIn && isPublicRoute) return '/';
    return null;
  },
  routes: [
    GoRoute(path: '/', builder: (context, state) => const HomeScreen()),
    GoRoute(path: '/login', builder: (context, state) => const LoginScreen()),
    GoRoute(path: '/register', builder: (context, state) => const RegisterScreen()),
    GoRoute(path: '/scan', builder: (context, state) => const RoomScanScreen()),
    GoRoute(
      path: '/design/:roomId',
      builder: (context, state) => DesignResultScreen(
        roomId: state.pathParameters['roomId']!,
        style: state.uri.queryParameters['style'],
      ),
    ),
    GoRoute(
      path: '/ar/:designId',
      builder: (context, state) => ARViewScreen(
        designId: state.pathParameters['designId']!,
      ),
    ),
    GoRoute(
      path: '/ar/house/:roomDesignId',
      builder: (context, state) => ARViewScreen(
        designId: state.pathParameters['roomDesignId']!,
        isHouseRoomDesign: true,
      ),
    ),
    GoRoute(
      path: '/cost/:designId',
      builder: (context, state) => CostEstimationScreen(
        designId: state.pathParameters['designId']!,
      ),
    ),
    GoRoute(
      path: '/furniture/:roomId',
      builder: (context, state) => FurnitureRecommendationScreen(
        roomId: state.pathParameters['roomId']!,
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
    GoRoute(path: '/feng-shui', builder: (context, state) => const FengShuiScreen()),
    GoRoute(path: '/seasonal', builder: (context, state) => const SeasonalThemeScreen()),
    GoRoute(path: '/pet-friendly', builder: (context, state) => const PetFriendlyScreen()),
    GoRoute(path: '/3d-walkthrough', builder: (context, state) => const Walkthrough3DScreen()),
    GoRoute(path: '/profile', builder: (context, state) => const ProfileScreen()),
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
